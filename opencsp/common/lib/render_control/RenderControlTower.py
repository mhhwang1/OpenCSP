import opencsp.common.lib.render_control.RenderControlPointSeq as rcps
import opencsp.common.lib.render_control.RenderControlText as rctxt
from opencsp.common.lib.render_control.RenderControlPointSeq import RenderControlPointSeq


class RenderControlTower:
    def __init__(
        self,
        centroid: bool = False,
        draw_name=False,
        name_style=rctxt.default(color='k'),
        draw_outline=True,
        point_styles: RenderControlPointSeq = rcps.marker(),
        wire_frame: RenderControlPointSeq = rcps.outline(),
        target: RenderControlPointSeq = rcps.marker(marker='x', color='r', markersize=6),
    ) -> None:

        super(RenderControlTower, self).__init__()

        self.centroid = centroid
        self.draw_name = draw_name
        self.name_style = name_style
        self.draw_outline = draw_outline
        self.point_styles = point_styles
        self.wire_frame = wire_frame
        self.target = target

    def style(self, any):
        """ "style" is a method commonly used by RenderControlEnsemble.
        We add this method here so that RenderControlHeliostat can be used similarly to RenderControlEnsemble."""
        return self


# Common Configurations


def normal_tower():
    # Overall tower outline only.
    return RenderControlTower()


def no_target():
    # tower outline with no target.
    return RenderControlTower(wire_frame=rcps.outline(color='g'), target=False)