from models.mongo.post import Post


class DashboardService:

    @classmethod
    async def get_posts_by_user(cls, user):
        posts = await Post.find(Post.user.id == user.id, fetch_links=True).to_list()
        return posts
    
    @classmethod
    async def get_posts_by_users(cls, users):
        posts = []
        for user in users:
            print(user.email)
            posts.extend(await cls.get_posts_by_user(user))
        return posts

