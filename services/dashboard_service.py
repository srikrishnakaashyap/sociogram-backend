from models.mongo.post import Post

class DashboardService:

    @classmethod
    async def get_posts_by_user(cls, user):
        posts = await Post.find(user=user)
        return posts