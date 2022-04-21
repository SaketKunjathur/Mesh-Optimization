import pygame, sys, numpy as np
from typing import NamedTuple

pygame.init()

width, height = 750, 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mesh Optimization")

bg_color = (43, 43, 43)

mesh_list = np.zeros((11, 11))

block_types = {"air": 0, "solid": 1}


class RectMesh(NamedTuple):
    left: bool = True
    right: bool = True
    top: bool = True
    bottom: bool = True


class RenderMesh(NamedTuple):
    mesh: RectMesh
    rect: pygame.Rect
    draw_block: tuple[int, int, int]
    color: tuple[int, int, int] = (0, 0, 0)
    meshwidth: int = 1

    def draw(self):
        pygame.draw.rect(win, self.draw_block, self.rect)
        if self.mesh.left:
            pygame.draw.line(
                win, self.color, self.rect.topleft, self.rect.bottomleft, self.meshwidth
            )
        if self.mesh.right:
            pygame.draw.line(
                win,
                self.color,
                self.rect.topright,
                self.rect.bottomright,
                self.meshwidth,
            )
        if self.mesh.top:
            pygame.draw.line(
                win, self.color, self.rect.topleft, self.rect.topright, self.meshwidth
            )
        if self.mesh.bottom:
            pygame.draw.line(
                win,
                self.color,
                self.rect.bottomleft,
                self.rect.bottomright,
                self.meshwidth,
            )


def optimizeMesh(
    mesh: tuple,
    mesh_width: int,
    mesh_height: int,
    blocks_dict: dict, 
    mesh_color: tuple[int, int, int] = (0, 0, 0),
    block_color: tuple[int, int, int] = bg_color,
) -> tuple:
    rect_w, rect_h = mesh_width // len(mesh[0]), mesh_height // len(mesh)
    new_mesh = []
    for c_idx, col in enumerate(mesh):
        for r_idx, row in enumerate(col):
            if row == blocks_dict['solid']:
                side_rects = RectMesh()
                if c_idx > 0 and mesh[c_idx - 1][r_idx] == 1:
                    side_rects = side_rects._replace(top=False)
                if c_idx < len(mesh) - 1 and mesh[c_idx + 1][r_idx] == 1:
                    side_rects = side_rects._replace(bottom=False)
                if r_idx > 0 and mesh[c_idx][r_idx - 1] == 1:
                    side_rects = side_rects._replace(left=False)
                if r_idx < len(mesh[0]) - 1 and mesh[c_idx][r_idx + 1] == 1:
                    side_rects = side_rects._replace(right=False)
                mesh_obj = RenderMesh(
                    side_rects,
                    pygame.Rect(r_idx * rect_w, c_idx * rect_h, rect_w, rect_h),
                    block_color,
                    mesh_color,
                    5,
                )
                new_mesh.append(mesh_obj)
    return new_mesh


optim_mesh = optimizeMesh(mesh_list, width, height, block_types, (0, 0, 0), (17, 93, 105))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    win.fill(bg_color)
    if pygame.mouse.get_pressed()[0]:
        pos = pygame.mouse.get_pos()
        dx, dy = pos[0] // (width // len(mesh_list[0])), pos[1] // (
            width // len(mesh_list)
        )
        if mesh_list[dy][dx] == 0:
            mesh_list[dy][dx] = 1
    if pygame.mouse.get_pressed()[2]:
        pos = pygame.mouse.get_pos()
        dx, dy = pos[0] // (width // len(mesh_list[0])), pos[1] // (
            width // len(mesh_list)
        )
        if mesh_list[dy][dx] == 1:
            mesh_list[dy][dx] = 0
    optim_mesh = optimizeMesh(mesh_list, width, height, block_types, (0, 0, 0), (17, 93, 105))
    for each in optim_mesh:
        each.draw()
    pygame.display.update()
