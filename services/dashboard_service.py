from models.mongo.post import Post
import asyncio
from concurrent.futures import ThreadPoolExecutor

class DashboardService:

    @classmethod
    async def get_posts_by_user(cls, user):
        posts = await Post.find(Post.user.id==user.id).to_list()
        return posts