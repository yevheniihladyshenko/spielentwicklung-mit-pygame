from dataclasses import dataclass

@dataclass
class Settings:
    width: int = 960
    height: int = 540
    fps: int = 60

    grid: int = 24
    difficulty: str = "Normal"  # Easy | Normal | Hard

    def tick_ms(self) -> int:
        return {
            "Easy": 140,
            "Normal": 110,
            "Hard": 85
        }.get(self.difficulty, 110)
