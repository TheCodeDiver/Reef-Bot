from discord.ext import commands

class TaskTracker(commands.Cog):
    """Cog for tracking user tasks"""

    def __init__(self, bot):
        self.bot = bot
        self.tasks = {}

    @commands.command()
    async def addtask(self, ctx, *, task: str):
        """Add a new task"""
        user_id = ctx.author.id
        self.tasks.setdefault(user_id, []).append(task)
        await ctx.send(f"✅ Task added for {ctx.author.display_name}: `{task}`")

    @commands.command()
    async def mytasks(self, ctx):
        """Show tasks"""
        user_id = ctx.author.id
        user_tasks = self.tasks.get(user_id, [])
        if not user_tasks:
            await ctx.send("You have no tasks.")
        else:
            tasks_formatted = "\n".join(f"- {t}" for t in user_tasks)
            await ctx.send(f"📋 **Your tasks:**\n{tasks_formatted}")

def setup(bot):
    bot.add_cog(TaskTracker(bot))
