from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText
from ya2.gameobject import Gui
from direct.gui.OnscreenImage import OnscreenImage


class _Gui(Gui):
    '''This class models the GUI component of a track.'''

    def __init__(self, mdt, minimap):
        Gui.__init__(self, mdt)
        self.debug_txt = OnscreenText(
            '', pos=(-.1, .1), scale=0.05, fg=(1, 1, 1, 1),
            parent=eng.a2dBottomRight, align=TextNode.ARight,
            font=eng.font_mgr.load_font('assets/fonts/zekton rg.ttf'))
        self.__wip_txt = OnscreenText(
            _('work in progress'), pos=(.1, .1), scale=0.05, fg=(1, 1, 1, 1),
            parent=eng.a2dBottomLeft, align=TextNode.ALeft,
            font=eng.font_mgr.load_font('assets/fonts/zekton rg.ttf'))
        self.__countdown_txt = OnscreenText(
            '', pos=(0, 0), scale=.2, fg=(1, 1, 1, 1),
            font=eng.font_mgr.load_font('assets/fonts/zekton rg.ttf'))
        self.__keys_img = OnscreenImage(
            image='assets/images/gui/keys.png', parent=eng.a2dTopLeft,
            pos=(.7, 1, -.4), scale=(.6, 1, .3))
        self.__keys_img.setTransparency(True)
        self.way_txt = OnscreenText(
            '', pos=(.1, .4), scale=0.1, fg=(1, 1, 1, 1),
            parent=eng.a2dBottomLeft, align=TextNode.ALeft,
            font=eng.font_mgr.load_font('assets/fonts/zekton rg.ttf'))
        self.countdown_cnt = 3
        self.minimap = OnscreenImage(
            'assets/images/minimaps/%s.jpg' % minimap, pos=(-.25, 1, .25),
            scale=.2, parent=eng.a2dBottomRight)
        self.car_handle = OnscreenImage(
            'assets/images/minimaps/car_handle.png', pos=(-.25, 1, .25),
            scale=.03, parent=eng.a2dBottomRight)
        self.car_handle.setTransparency(True)
        self.set_corners()
        taskMgr.doMethodLater(1.0, self.process_countdown, 'coutdown')

    def set_corners(self):
        corners = ['topleft', 'topright', 'bottomright', 'bottomleft']
        corners = [self.mdt.gfx.model.find('**/Minimap'+corner) for corner in corners]
        if not any(corner.isEmpty() for corner in corners):
            self.corners = [corner.get_pos() for corner in corners]

    def update_minimap(self):
        if not hasattr(self, 'corners'):
            return
        left = self.corners[0].getX()
        right = self.corners[1].getX()
        top = self.corners[0].getY()
        bottom = self.corners[3].getY()
        car_pos = game.car.gfx.nodepath.get_pos()
        pos_x_norm = (car_pos.getX() - left) / (right - left)
        pos_y_norm = (car_pos.getY() - bottom) / (top - bottom)

        width = self.minimap.getScale()[0] * 2.0
        height = self.minimap.getScale()[2] * 2.0
        center_x = self.minimap.getX()
        center_y = self.minimap.getZ()
        left_img = center_x - width / 2.0
        bottom_img = center_y - height / 2.0
        pos_x = left_img + pos_x_norm * width
        pos_y = bottom_img + pos_y_norm * height
        self.car_handle.set_pos(pos_x, 1, pos_y)
        self.car_handle.setR(-game.car.gfx.nodepath.getH())

    def process_countdown(self, task):
        if self.countdown_cnt >= 0:
            self.mdt.audio.countdown_sfx.play()
            txt = str(self.countdown_cnt) if self.countdown_cnt else _('GO!')
            self.__countdown_txt.setText(txt)
            self.countdown_cnt -= 1
            return task.again
        else:
            self.__countdown_txt.destroy()
            destroy_keys = lambda task: self.__keys_img.destroy()
            taskMgr.doMethodLater(5.0, destroy_keys, 'destroy keys')
            game.track.fsm.demand('Race')

    def show_results(self):
        self.result_img = OnscreenImage(image='assets/images/gui/results.png',
                                        scale=(.8, 1, .8))
        self.result_img.setTransparency(True)
        self.__res_txts = [OnscreenText(
            str(game.car.logic.lap_times[i-1]) if i else '',
            pos=(.3, .2 - .2 * i), scale=.1, fg=(.75, .75, .75, 1),
            font=eng.font_mgr.load_font('assets/fonts/zekton rg.ttf'))
            for i in range(4)]
        self.__res_txts += [OnscreenText(
            _('LAP'), pos=(-.3, .35), scale=.1, fg=(.75, .75, .75, 1),
            font=eng.font_mgr.load_font('assets/fonts/zekton rg.ttf'))
            for i in range(4)]
        self.__res_txts += [OnscreenText(
            str(i), pos=(-.3, .2 - .2 * i), scale=.1, fg=(.75, .75, .75, 1),
            font=eng.font_mgr.load_font('assets/fonts/zekton rg.ttf'))
            for i in range(1, 4)]
        def to_menu(task):
            map(lambda txt: txt.destroy(), self.__res_txts)
            self.result_img.destroy()
            game.fsm.demand('Menu')
        taskMgr.doMethodLater(10.0, to_menu, 'to menu')

    def destroy(self):
        Gui.destroy(self)
        self.__wip_txt.destroy()
        self.way_txt.destroy()
        self.minimap.destroy()
        self.car_handle.destroy()