from skills.image_generator import generate_image
from skills.ppt_image_skill import generate_ppt
from skills.youtube_analysis_skill import analyze_youtube

class SkillsManager:
    @staticmethod
    async def run_skill(skill_name, *args, **kwargs):
        if skill_name == "image":
            return await generate_image(*args, **kwargs)
        elif skill_name == "ppt":
            return await generate_ppt(*args, **kwargs)
        elif skill_name == "youtube":
            return await analyze_youtube(*args, **kwargs)
        else:
            raise ValueError(f"Unknown skill: {skill_name}")
