# encoding: utf-8

###########################################################################################################
#
#
#	Palette Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#
###########################################################################################################

from GlyphsApp.plugins import *
from vanilla import *
from AppKit import NSNotificationCenter, NSSwitchButton, NSShadowlessSquareBezelStyle, NSLeftTextAlignment, NSNoCellMask
import traceback

# print "Reporter Toggler 2017-11-06"


def ReporterSort(obj1, obj2):
	return cmp(obj1.title(), obj2.title())


########################################
########################################
########################################
# Classes almost exactly as in the vanilla LIB
# @ https://github.com/typesupply/vanilla/blob/master/Lib/vanilla/vanillaCheckBox.py
#
# Basically I just aim for a change of pos values for style `mini` at `textBoxPosSize` 
#
# --> All this code can be removed* to use a classic vanilla style CheckBox, also change
# checkBox = MFCheckBox( (10, elementHeight*i, ...
# back to:
# checkBox = CheckBox( (10, elementHeight*i, ...
#
# *) Also can be removed if Typesupply accepts my pull request to change these values
# [https://github.com/typesupply/vanilla/pull/36]

class _CheckBoxManualBuildButton(Button):

    nsButtonType = NSSwitchButton
    frameAdjustments = {
        "regular": (-2, -3, 4, 4),
        "small": (-3, -7, 5, 4),
        "mini": (-3, -11, 6, 8),
        }

    def set(self, value):
        self._nsObject.setState_(value)

    def get(self):
        return self._nsObject.state()

    def toggle(self):
        state = self.get()
        self.set(not state)


class _CheckBoxManualBuildTextButton(Button):

    nsBezelStyle = NSShadowlessSquareBezelStyle
    frameAdjustments = None

    def __init__(self, posSize, title, callback, sizeStyle):
        super(_CheckBoxManualBuildTextButton, self).__init__(posSize, title=title, callback=callback)
        self._nsObject.setBordered_(False)
        self._setSizeStyle(sizeStyle)
        self._nsObject.setAlignment_(NSLeftTextAlignment)
        self._nsObject.cell().setHighlightsBy_(NSNoCellMask)

########################################


class MFCheckBox(CheckBox):

	allFrameAdjustments = {
		"mini": (0, -4, 0, 8),
		"small": (0, -2, 0, 4),
		"regular": (0, -2, 0, 4),
		}

	def __init__(self, posSize, title, callback=None, value=False, sizeStyle="regular"):

		# super(MFCheckBox, self).__init__(posSize, title, callback=None, value=False, sizeStyle=chosenSize)

		self._setupView("NSView", posSize)

		self._callback = callback

		buttonSizes = {
				"mini": (10, 10),
				"small": (18, 18),
				"regular": (22, 22)
				}
		left, top, width, height = posSize

		self.frameAdjustments = self.allFrameAdjustments[sizeStyle]

		buttonWidth, buttonHeight = buttonSizes[sizeStyle]
		buttonLeft, buttonTop = self.frameAdjustments[:2]
		buttonLeft= abs(buttonLeft)
		buttonTop = abs(buttonTop)

		# adjust the position of the text button in relation to the check box
		textBoxPosSize = {
				# left, top, height
				## ************************
				"mini": (12, 5, 12), # Changed by Mark, original: (10, 4, 12)
				"small": (14, 6, 14), # Changed by Mark, original: (14, 4, 14)
				## ************************
				"regular": (16, 3, 17)
				}
		textBoxLeft, textBoxTop, textBoxHeight = textBoxPosSize[sizeStyle]
		textBoxWidth = 0

		self._checkBox = _CheckBoxManualBuildButton((0, 0, buttonWidth, buttonHeight), "", callback=self._buttonHit, sizeStyle=sizeStyle)
		self._checkBox.set(value)

		self._textButton = _CheckBoxManualBuildTextButton((textBoxLeft, textBoxTop, textBoxWidth, textBoxHeight), title=title, callback=self._buttonHit, sizeStyle=sizeStyle)
		######


		### Added by Mark:
		try:
			nsbutton = self._textButton.getNSButton()
			## Optional Button Styles
			# nsbutton.setBordered_(1)
			# nsbutton.setBezelStyle_(1)
			# nsbutton.setButtonType_(0) # 1 is funky
			# nsbutton.setAlignment_(0)
		except:
			print traceback.format_exc()

########################################
########################################
########################################		






'''
# Under Construction, not working.
# Attempt to reduce code above.
class _CheckBoxManualBuild(VanillaBaseObject):
	textBoxPosSize = {
			# left, top, height
			## ************************
			"mini": (12, 5, 12), # Changed by Mark, original: (10, 4, 12)
			"small": (14, 6, 14), # Changed by Mark, original: (14, 4, 14)
			## ************************
			"regular": (16, 3, 17)
			}
	def __init__(self, posSize, title, callback=None, value=False, sizeStyle="regular"):
		super(_CheckBoxManualBuild, self).__init__()
		print "Class B"
		print self.textBoxPosSize
class M2FCheckBox(_CheckBoxManualBuild):
	def __init__(self, posSize, title, callback=None, value=False, sizeStyle="regular"):
		super(M2FCheckBox, self).__init__(posSize, title, callback=None, value=False, sizeStyle="regular")
		print "Class C"
		print self.textBoxPosSize
'''









elmtSizes = {  # 14 for mini, 16 for small # in older versions we had small/15; but larger leading is easier to read
	'mini' : 14,
	'small' : 16,
}
chosenSize = 'mini'



class ReporterToggler (PalettePlugin):

	def settings(self):
		try:
			self.name = 'Reporters'
			# Vanilla window and group with controls
			width = 160 # 150
			elementHeight = elmtSizes[chosenSize]
			height = len(Glyphs.reporters) * elementHeight # 900
			self.paletteView = Window((width, height + 10))
			self.paletteView.group = Group((0, 0, width, height + 10))
			# self.paletteView.group.text = TextBox((10, 0, -10, -10), self.name, sizeStyle='mini')
			self.reporterArray = list(Glyphs.reporters)
			self.reporterArray = sorted(self.reporterArray, ReporterSort)

			for i, reporter in enumerate(self.reporterArray): # Glyphs.activeReporters
				if reporter in Glyphs.activeReporters:
					isActive = True
				else:
					isActive = False
				# print reporter.classCode()
				attrName = "CheckBox_%s" % str(i)
				try:
					checkBox = MFCheckBox( (10, elementHeight*i, -10, elementHeight), reporter.title(), sizeStyle=chosenSize, value=isActive, callback=self.toggle )
				except:
					checkBox = CheckBox( (10, elementHeight*i, -10, elementHeight), reporter.title(), sizeStyle=chosenSize, value=isActive, callback=self.toggle )
				setattr(self.paletteView.group, attrName, checkBox)

			# Set dialog to NSView
			self.dialog = self.paletteView.group.getNSView()
		except:
			print traceback.format_exc() # self.logToConsole(traceback.format_exc())


	def start(self):
		# Adding a callback for the 'GSUpdateInterface' event
		s = objc.selector( self.update, signature="v@:" )
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSUpdateInterface", None )  # GSDocumentCloseNotification | GSDocumentActivateNotification


	def toggle(self, sender):
		try:
			thisReporter = sender.getTitle()
			for i, rep in enumerate(self.reporterArray):
				if rep.title() == thisReporter:
					if sender.get() == 0:
						Glyphs.deactivateReporter(rep)
					if sender.get() == 1:
						Glyphs.activateReporter(rep)
		except:
			print traceback.format_exc()


	def update( self, sender ):
		try:
			for i, reporter in enumerate(self.reporterArray): # Glyphs.activeReporters
				if reporter in Glyphs.activeReporters:
					isActive = True
				else:
					isActive = False
				exec("self.paletteView.group.CheckBox_"+str(i)+".set("+str(isActive)+")")
		except:
			print traceback.format_exc()

	def quit(self):
		# Delete callbacks when Glyphs quits, otherwise it'll crash :( 
		NSNotificationCenter.defaultCenter().removeObserver_(self)
