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

import objc
from GlyphsApp.plugins import *
from vanilla import *
from AppKit import NSNotificationCenter, NSSwitchButton, NSShadowlessSquareBezelStyle, NSLeftTextAlignment, NSNoCellMask
import traceback

print "Reporter Toggler 2018-01-29"


def ReporterSort(obj1, obj2):
	return cmp(obj1.title(), obj2.title())



elmtSizes = {  # 14 for mini, 16 for small # in older versions we had small/15; but larger leading is easier to read
	'mini' : 15, # 14
	'small' : 16,
}
chosenSize = 'mini'



# CheckBox.frameAdjustments = {
# 		"mini": (0, -4, 0, 8),
# 		"small": (0, -2, 0, 4),
# 		"regular": (0, -2, 0, 4),
# 		}


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

				checkBox = CheckBox( (10, elementHeight*i, -10, elementHeight), reporter.title(), sizeStyle=chosenSize, value=isActive, callback=self.toggle )
				setattr(self.paletteView.group, attrName, checkBox)

			# Set dialog to NSView
			self.dialog = self.paletteView.group.getNSView()
		except:
			print traceback.format_exc() # self.logToConsole(traceback.format_exc())


	def start(self):
		# Adding a callback for when the visiblity of a reporter changes
		NSUserDefaults.standardUserDefaults().addObserver_forKeyPath_options_context_(self, "visibleReporters", 0, None)

	def observeValueForKeyPath_ofObject_change_context_(self, keyPath, aObject, change, context):
		self.update(self)

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
		NSUserDefaults.standardUserDefaults().removeObserver_forKeyPath_(self, "visibleReporters")

