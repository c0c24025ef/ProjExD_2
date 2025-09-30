import os
import sys
import random
import pygame
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRect or ばくだんRect
    戻り値：判定結果タプル（横方向，縦方向）
    画面内ならTrue／画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向にはみ出ていたら
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: # 縦方向にはみ出ていたら
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    # こうかとんの画像を準備
    kk_img_orig = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_img_flipped = pg.transform.flip(kk_img_orig, True, False) # 左右反転
    kk_imgs = {
        (0, 0): kk_img_orig, # 静止
        (5, 0): kk_img_orig, # 右
        (5, -5): pg.transform.rotozoom(kk_img_orig, -45, 1.0), # 右上
        (0, -5): pg.transform.rotozoom(kk_img_orig, -90, 1.0), # 上
        (-5, -5): pg.transform.rotozoom(kk_img_flipped, -45, 1.0), # 左上
        (-5, 0): kk_img_flipped, # 左
        (-5, 5): pg.transform.rotozoom(kk_img_flipped, 45, 1.0), # 左下
        (0, 5): pg.transform.rotozoom(kk_img_orig, 90, 1.0), # 下
        (5, 5): pg.transform.rotozoom(kk_img_orig, 45, 1.0), # 右下
    }
    kk_img = kk_img_orig
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
 

    # 爆弾の元画像を準備
    bb_img_orig = pg.Surface((20, 20), pg.SRCALPHA)
    pg.draw.circle(bb_img_orig, (255, 0, 0), (10, 10), 10)
   
    
    bb_rct = bb_img_orig.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        screen.blit(bg_img, [0, 0])

        if kk_rct.colliderect(bb_rct):
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        if tuple(sum_mv) in kk_imgs:
            kk_img = kk_imgs[tuple(sum_mv)]

        screen.blit(kk_img, kk_rct)

        # 爆弾の拡大・加速処理
        zoom_factor = 1 + (tmr / 5000)
        speed_factor = 1 + (tmr / 2000)
        
        bb_img = pg.transform.rotozoom(bb_img_orig, 0, zoom_factor)
        bb_rct = bb_img.get_rect(center=bb_rct.center)

        avx = vx * speed_factor
        avy = vy * speed_factor
        bb_rct.move_ip(avx, avy)
        
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()