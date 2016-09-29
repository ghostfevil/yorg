from panda3d.core import getModelPath


class GfxMgr:

    def __init__(self, aa):
        getModelPath().appendDirectory('assets/models')
        eng.enableParticles()
        render.setShaderAuto()
        render.setTwoSided(True)
        if aa:
            render.setAntialias(AntialiasAttrib.MAuto)

    @staticmethod
    def __set_toon():
        '''Sets toon shading.'''
        tempnode = NodePath(PandaNode('temp node'))
        tempnode.setAttrib(LightRampAttrib.makeSingleThreshold(.5, .4))
        tempnode.setShaderAuto()
        base.cam.node().setInitialState(tempnode.getState())
        CommonFilters(base.win, base.cam).setCartoonInk(separation=1)

    def print_stats(self):
        '''Prints rendering stats.'''
        print '\n\n#####\nrender2d.analyze()'
        self.render2d.analyze()
        print '\n\n#####\nrender.analyze()'
        self.render.analyze()
        print '\n\n#####\nrender2d.ls()'
        self.render2d.ls()
        print '\n\n#####\nrender.ls()'
        self.render.ls()

    @staticmethod
    def particle(path, parent, render_parent, pos, timeout):
        '''Does a particle effect.'''
        par = ParticleEffect()
        par.loadConfig(path)
        par.start(parent=parent, renderParent=render_parent)
        par.setPos(pos)
        args = (timeout, lambda par: par.cleanup(), 'clear', [par])
        taskMgr.doMethodLater(*args)