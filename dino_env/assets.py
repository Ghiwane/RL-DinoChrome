import os
import pygame

# Calcul des chemins d'accès vers le dossier racine des assets
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


def _trim_transparent(surface):
    """
    Recadre une surface sur son contenu non-transparent réel (min_alpha=10)
    afin d'éliminer les marges vides autour des sprites PNG.
    """
    rect = surface.get_bounding_rect(min_alpha=10)
    if rect.width == 0 or rect.height == 0:
        return surface
    return surface.subsurface(rect).copy()


def _load(relative_path, size=None):
    """
    Charge une image, supprime ses bordures transparentes et la redimensionne
    éventuellement aux dimensions exactes fournies (largeur, hauteur).
    """
    full_path = os.path.join(ASSETS_DIR, relative_path)
    img = pygame.image.load(full_path).convert_alpha()
    img = _trim_transparent(img)
    if size is not None:
        img = pygame.transform.smoothscale(img, size)
    return img


def _load_keep_ratio_width(relative_path, target_width):
    """
    Charge une image et la redimensionne en conservant son ratio d'aspect d'origine,
    en se basant uniquement sur la largeur cible.
    """
    full_path = os.path.join(ASSETS_DIR, relative_path)
    raw = pygame.image.load(full_path).convert_alpha()
    raw = _trim_transparent(raw)
    ratio = target_width / raw.get_width()
    target_height = int(raw.get_height() * ratio)
    return pygame.transform.smoothscale(raw, (target_width, target_height))


def load_assets():
    """
    Charge et centralise l'ensemble des sprites du jeu dans un dictionnaire
    en appliquant les dimensions définies dans constants.py.
    """
    import constants as ct

    dino_run_size = (ct.DINO_RUNNING_W, ct.DINO_RUNNING_H)

    return {
        # Sprites d'animation du Dinosaure
        "dino_running": [
            _load("dino/dino_running1.png", dino_run_size),
            _load("dino/dino_running2.png", dino_run_size),
        ],
        "dino_ducking": [
            _load_keep_ratio_width("dino/dino_ducking1.png", ct.DINO_DUCKING_W),
            _load_keep_ratio_width("dino/dino_ducking2.png", ct.DINO_DUCKING_W),
        ],
        "dino_jumping": _load("dino/dino_jumping.png", dino_run_size),
        "dino_dead": _load("dino/dino_dead.png", dino_run_size),

        # Sprites des Cactus (Grands et Petits)
        "cactus": [
            _load("cactus/BigCactus1.png", (ct.BIGCACTUS1_W, ct.BIGCACTUS_H)),
            _load("cactus/BigCactus2.png", (ct.BIGCACTUS2_W, ct.BIGCACTUS_H)),
            _load("cactus/BigCactus3.png", (ct.BIGCACTUS3_W, ct.BIGCACTUS_H)),
            _load("cactus/BigCactus4.png", (ct.BIGCACTUS4_W, ct.BIGCACTUS_H)),
            _load("cactus/SmallCactus1.png", (ct.SMALLCACTUS1_W, ct.SMALLCACTUS_H)),
            _load("cactus/SmallCactus2.png", (ct.SMALLCACTUS2_W, ct.SMALLCACTUS_H)),
            _load("cactus/SmallCactus3.png", (ct.SMALLCACTUS3_W, ct.SMALLCACTUS_H)),
        ],

        # Sprites des Ptérodactyles
        "ptero": [
            _load("Ptera/ptera1.png", (ct.PTERO_W, ct.PTERO_H)),
            _load("Ptera/ptera2.png", (ct.PTERO_W, ct.PTERO_H)),
        ],

        # Éléments de décor et d'interface
        "ground": _load("decor/ground.png"),
        "cloud": _load("decor/cloud.png", (70, 30)),
        "game_over": _load("hud/game_over.png"),
    }