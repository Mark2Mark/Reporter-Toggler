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
from AppKit import NSStackView, NSButton, NSBundle, NSOnState, NSOffState, NSMiniControlSize, NSSmallControlSize
import traceback
NSStackViewGravityLeading = 1
NSLayoutConstraintOrientationVertical = 1
NSLayoutConstraintOrientationHorizontal = 0
# print "Reporter Toggler 2018-01-29"

ControllSize = NSMiniControlSize # NSSmallControlSize


def ReporterSort(obj1, obj2):
	return cmp(obj1.title(), obj2.title())

class ReporterToggler (PalettePlugin):
	stackView = objc.IBOutlet()
	view = objc.IBOutlet()
	def settings(self):
		try:
			#NSBundle.loadNibNamed_owner_('View', self)
			self.name = 'Reporters'
			
			width = 160
			self.reporterArray = list(Glyphs.reporters)
			self.reporterArray = sorted(self.reporterArray, ReporterSort)
			
			
			
			self.checkboxes = []
			for i, reporter in enumerate(self.reporterArray): # Glyphs.activeReporters
				# print reporter.classCode()
				
				checkBox = NSButton.checkboxWithTitle_target_action_(reporter.title(), self, self.toggle)
				
				if reporter in Glyphs.activeReporters:
					isActive = NSOnState
				else:
					isActive = NSOffState
				checkBox.setState_(isActive)
				checkBox.setControlSize_(ControllSize)
				font = NSFont.systemFontOfSize_(NSFont.systemFontSizeForControlSize_(ControllSize))
				checkBox.setFont_(font)
				self.checkboxes.append(checkBox)
			self.dialog = NSStackView.stackViewWithViews_(self.checkboxes)
			self.dialog.setOrientation_(1)
			self.dialog.setAlignment_(1)
			self.dialog.setSpacing_(5)
			self.dialog.setEdgeInsets_((2, 8, 8, 1))
			self.dialog.setClippingResistancePriority_forOrientation_(250, NSLayoutConstraintOrientationHorizontal)
			self.dialog.setViews_inGravity_(self.checkboxes, NSStackViewGravityLeading)
			self.dialog.setNeedsLayout_(True)
			#self.dialog = self.view

		except:
			print traceback.format_exc()


	def start(self):
		# Adding a callback for when the visiblity of a reporter changes
		NSUserDefaults.standardUserDefaults().addObserver_forKeyPath_options_context_(self, "visibleReporters", 0, None)


	def observeValueForKeyPath_ofObject_change_context_(self, keyPath, aObject, change, context):
		self.update(self)


	def toggle(self, sender):
		try:
			thisReporter = sender.title()
			for i, reporter in enumerate(self.reporterArray):
				if reporter.title() == thisReporter:
					if sender.state() == NSOffState:
						Glyphs.deactivateReporter(reporter)
					else:
						Glyphs.activateReporter(reporter)
		except:
			print traceback.format_exc()


	def update(self, sender):
		try:
			for i, reporter in enumerate(self.reporterArray): # Glyphs.activeReporters
				if reporter in Glyphs.activeReporters:
					isActive = NSOnState
				else:
					isActive = NSOffState
				self.checkboxes[i].setState_(isActive)
		except:
			print traceback.format_exc()

	def __del__(self):
		# Delete callbacks when the window is closed, otherwise it'll crash :( 
		NSUserDefaults.standardUserDefaults().removeObserver_forKeyPath_(self, "visibleReporters")

