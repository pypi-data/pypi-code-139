import sdl2.ext
from shikkoku.app import App
from shikkoku.sample_scene import SampleScene
from shikkoku.menu_scene import MenuScene
from shikkoku.cc_scene import CCScene
from shikkoku.game_scene import GameScene

def main():
    """Main game entry point."""
    
    with App("Game", (1200, 800)) as app:
        app.assign_resource_path("shikkoku.resources")
        scene = SampleScene(app, "test")
        mscene = MenuScene(app, "menu")
        app.add_scene(scene)
        app.add_scene(mscene)
        app.add_scene(GameScene(app,"game"))
        app.add_scene(CCScene(app, "cc"))
        app.start_game_loop(mscene)
    
main()