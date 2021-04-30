import os
from pygame import mixer, error
# from pygame.compat import geterror

main_dir = os.path.split(os.path.abspath(__file__))[0]
sound_dir = os.path.join(main_dir, '../sound')


def load_sound(name, volume):
    class NoneSound:
        def play(self): pass

    if not mixer or not mixer.get_init():
        return NoneSound()
    fullname = os.path.join(sound_dir, name)
    try:
        sound = mixer.Sound(fullname)
        sound.set_volume(volume)
    except error:
        print('Cannot load sound: %s' % fullname)
        # raise SystemExit(str(geterror()))
        sound = NoneSound()
    return sound


def load_music(name, volume):
    class NoneSound:
        def play(self): pass

    if not mixer or not mixer.get_init():
        return NoneSound()
    fullname = os.path.join(sound_dir, name)
    try:
        mixer.music.load(fullname)
        mixer.music.set_volume(volume)
    except error:
        print('Cannot load music: %s' % fullname)
        # raise SystemExit(str(geterror()))

