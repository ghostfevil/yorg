'''This module defines the main page.'''
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
from .page import Page, PageGui
from .imgbtn import ImageButton


class MainPageGui(PageGui):
    '''This class models the GUI component of a page.'''

    def build(self):
        self.__build_social()
        self.__build_version()

    def __build_social(self):
        '''Sets social buttons.'''
        sites = [
            ('facebook', 'http://www.facebook.com/Ya2Tech'),
            ('twitter', 'http://twitter.com/ya2tech'),
            ('google_plus', 'https://plus.google.com/118211180567488443153'),
            ('youtube',
             'http://www.youtube.com/user/ya2games?sub_confirmation=1'),
            ('pinterest', 'http://www.pinterest.com/ya2tech'),
            ('tumblr', 'http://ya2tech.tumblr.com'),
            ('feed', 'http://www.ya2.it/feed-following')]
        menu_gui = self.menu.gui
        menu_args = self.menu.gui.menu_args
        self.widgets += [
            ImageButton(
                parent=eng.base.a2dBottomRight, scale=.1,
                pos=(-1.0 + i*.15, 1, .1), frameColor=(0, 0, 0, 0),
                image=menu_args.social_path % site[0],
                command=eng.gui.open_browser, extraArgs=[site[1]],
                rolloverSound=menu_gui.rollover,
                clickSound=menu_gui.click)
            for i, site in enumerate(sites)]

    def __build_version(self):
        '''Sets the version.'''
        menu_gui = self.menu.gui
        self.widgets += [OnscreenText(
            text=eng.logic.version, parent=eng.base.a2dBottomLeft,
            pos=(.02, .02), scale=.04, fg=(.8, .8, .8, 1),
            align=TextNode.ALeft, font=menu_gui.font)]


class MainPage(Page):
    '''This class models a page.'''
    gui_cls = MainPageGui
