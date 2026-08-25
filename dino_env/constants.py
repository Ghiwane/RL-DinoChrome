# --- MOTEUR PHYSIQUE & DEPLACEMENT ---
GRAVITY = 1.1             # Accélération verticale appliquée au saut
Y_VELOCITY = -18.0        # Impulsion initiale du saut (négative = vers le haut)
SPEED = 12.0              # Vitesse initiale du défilement au sol
MAX_SPEED = 25.0          # Vitesse maximale atteignable
SPEED_DROP_COEF = 2.0     # Multiplicateur de gravité lors d'une chute rapide (FAST_FALLING)

# --- REPERES DU DECOR ET REFRESH ---
GROUND_Y = 260            # Ligne de sol de référence (en pixels depuis le haut)
GROUND_VISUAL_OFFSET = 0  # Ajustement vertical pour le rendu du sol

SCREEN_W = 900            # Largeur de la fenêtre Pygame
SCREEN_H = 300            # Hauteur de la fenêtre Pygame
FPS = 60                  # Nombre d'images par seconde

# --- DINOSAURE (DIMENSIONS ET SPAWN) ---
DINO_X = 60.0             # Position X fixe du dino à l'écran
DINO_RUNNING_W = 50       # Largeur de la hitbox en course
DINO_RUNNING_H = 60       # Hauteur de la hitbox en course
DINO_DUCKING_W = 75       # Largeur de la hitbox accroupie
DINO_DUCKING_H = 35       # Hauteur de la hitbox accroupie

# Position Y initiale du Dino ancrée sur GROUND_Y (+15 de marge d'enfoncement)
DINO_Y = GROUND_Y - DINO_RUNNING_H + 15

# --- OBSTACLES : PTERODACTYLES ---
PTERO_Y_HIGH = 100.0      # Altitude haute (nécessite d'être debout/courir)
PTERO_Y_MID = 190.0       # Altitude moyenne (nécessite de s'accroupir)
PTERO_Y_LOW = 215.0       # Altitude basse (nécessite de sauter par-dessus)
PTERO_W = 50              # Largeur de la hitbox du ptérodactyle
PTERO_H = 40              # Hauteur de la hitbox du ptérodactyle

# --- OBSTACLES : CACTUS ---
BIGCACTUS_H = 50          # Hauteur des grands cactus
BIGCACTUS1_W = 26         # Largeur pour 1 grand cactus
BIGCACTUS2_W = 50         # Largeur pour 2 grands cactus
BIGCACTUS3_W = 76         # Largeur pour 3 grands cactus
BIGCACTUS4_W = 75         # Largeur pour groupe de grands cactus

SMALLCACTUS_H = 35        # Hauteur des petits cactus
SMALLCACTUS1_W = 17       # Largeur pour 1 petit cactus
SMALLCACTUS2_W = 34       # Largeur pour 2 petits cactus
SMALLCACTUS3_W = 51       # Largeur pour 3 petits cactus

# --- PROGRESSION ET ACCELERATION ---
SPEED_INCREMENT = 1.0     # Augmentation de la vitesse à chaque palier
SCORE_PER_SPEEDUP = 100   # Nombre de points requis pour accélérer

# --- DELAIS D'APPARITION DES OBSTACLES (SPAWNER) ---
# Intervalle de réapparition (exprimé en nombre de frames)
SPAWN_MIN_FRAMES = 45     # Temps d'attente minimal entre 2 obstacles
SPAWN_MAX_FRAMES = 90     # Temps d'attente maximal entre 2 obstacles