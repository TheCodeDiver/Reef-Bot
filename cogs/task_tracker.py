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


    @commands.command(name="deletetask")
    async def delete_task(self, ctx, task_number: int):
        user_id = str(ctx.author.id)
        user_tasks = self.tasks.get(user_id, [])

        if 0 < task_number <= len(user_tasks):
            removed_task = self.tasks[user_id].pop(task_number - 1)
            save_tasks(self.tasks)
            await ctx.send(f"🗑️ Deleted task {task_number}: `{removed_task['task']}`")
        else:
            await ctx.send("⚠️ Invalid task number.")


    @commands.command(name="updatetask")
    async def update_task(self, ctx, task_number: int, *, new_description: str):
        user_id = str(ctx.author.id)
        user_tasks = self.tasks.get(user_id, [])

        if 0 < task_number <= len(user_tasks):
            old_description = user_tasks[task_number - 1]["task"]
            self.tasks[user_id][task_number - 1]["task"] = new_description
            save_tasks(self.tasks)
            await ctx.send(f"✏️ Task {task_number} updated:\n**Before:** {old_description}\n**After:** {new_description}")
        else:
            await ctx.send("⚠️ Invalid task number.")

    @commands.command(name="cleartasks")
    async def clear_tasks(self, ctx):
        user_id = str(ctx.author.id)

        if user_id in self.tasks and self.tasks[user_id]:
            self.tasks[user_id] = []
            save_tasks(self.tasks)
            await ctx.send("🧼 All your tasks have been cleared.")
        else:
            await ctx.send("📭 You don't have any tasks to clear.")


async def setup(bot):
    await bot.add_cog(TaskTracker(bot))
