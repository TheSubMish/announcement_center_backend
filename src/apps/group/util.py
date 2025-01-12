from src.apps.group.models import AnnouncementGroup
from src.apps.auth.models import User
from src.apps.analytics.models import GroupImpression


from django.db.models import Count

def recommend_groups_for_user(user, top_n=5):
    # Step 1: Group-Based Sorting
    # Count unique users interacting with each group and rank by unique user count
    groups_nearby = AnnouncementGroup.objects.annotate(
        unique_user_count=Count('groupimpression__user', distinct=True)
    ).order_by('-unique_user_count')

    # Step 2: User-Specific Group Recommendation
    # Exclude groups already interacted with by the user
    user_interacted_groups = GroupImpression.objects.filter(user=user).values_list('group_id', flat=True)
    groups_to_recommend = groups_nearby.exclude(id__in=user_interacted_groups)

    # Step 3: Collaborative Filtering for Groups
    # Identify similar users based on group interactions
    similar_users = User.objects.filter(
        groupimpression__group__in=user_interacted_groups
    ).exclude(id=user.id).distinct()

    # Fetch groups interacted with by similar users
    collaborative_groups = AnnouncementGroup.objects.filter(
        groupimpression__user__in=similar_users
    ).exclude(id__in=user_interacted_groups)

    # Rank remaining groups based on total interactions and unique user count
    final_recommendations = groups_to_recommend | collaborative_groups
    final_recommendations = final_recommendations.annotate(
        total_interactions=Count('groupimpression'),
        unique_user_count=Count('groupimpression__user', distinct=True)
    ).order_by('-total_interactions', '-unique_user_count')

    return final_recommendations[:top_n]

# Example usage:
# recommended_groups = recommend_groups_for_user(request.user, location="Kathmandu", top_n=5)
# for group in recommended_groups:
#     print(group.name)
