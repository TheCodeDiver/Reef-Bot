import discord
from discord.ext import commands
import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)


class TaskTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tasks = load_tasks()

    @commands.command(name="addtask")
    async def add_task(self, ctx, *, task: str):
        user_id = str(ctx.author.id)
        self.tasks.setdefault(user_id, []).append({"task": task, "done": False})
        save_tasks(self.tasks)
        await ctx.send(f"✅ Task added: `{task}`")

    @commands.command(name="tasks")
    async def list_tasks(self, ctx):
        user_id = str(ctx.author.id)
        user_tasks = self.tasks.get(user_id, [])
        if not user_tasks:
            await ctx.send("📭 You have no tasks.")
            return

        msg = "**Your Tasks:**\n"
        for idx, task in enumerate(user_tasks, 1):
            status = "✅" if task["done"] else "❌"
            msg += f"{idx}. {status} {task['task']}\n"

        await ctx.send(msg)

    @commands.command(name="completetask")
    async def complete_task(self, ctx, task_number: int):
        user_id = str(ctx.author.id)
        user_tasks = self.tasks.get(user_id, [])
        if 0 < task_number <= len(user_tasks):
            self.tasks[user_id][task_number - 1]["done"] = True
            save_tasks(self.tasks)
            await ctx.send(f"🎉 Task {task_number} marked as complete!")
        else:
            await ctx.send("⚠️ Invalid task number.")

async def setup(bot):
    await bot.add_cog(TaskTracker(bot))
