from enum import Enum, auto

class Si(Enum):
    # the namespace of SiliconUI
    # Flags for SiWidget
    FlashOnHintUpdated = auto()         # Make the tooltip flash when it is reset
    InstantMove = auto()                # Whether to move immediately without running animation
    InstantResize = auto()              # Whether to resize immediately without running animation
    InstantSetOpacity = auto()          # Whether to reset transparency immediately without running an animation
    HasMoveLimits = auto()              # Are there restricted movement areas?
    AdjustSizeOnTextChanged = auto()    # Whether to automatically adjust the space size when setText is called
    EnableAnimationSignals = auto()     # Whether to enable moved, resized, and opacityChanged signals
    DeleteOnHidden = auto()             # The next time it is hidden, run deleteLater()
    DeleteCenterWidgetOnCenterWidgetHidden = auto()  # The next time the center widget is hidden, run centerWidget().deleteLater()
