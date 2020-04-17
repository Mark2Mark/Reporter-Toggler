# encoding: utf-8
from __future__ import division, print_function, unicode_literals

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
from AppKit import NSStackView, NSButton, NSBundle, NSOnState, NSOffState, NSMiniControlSize, NSSmallControlSize, NSSwitchButton
import traceback
NSStackViewGravityLeading = 1
NSLayoutConstraintOrientationVertical = 1
NSLayoutConstraintOrientationHorizontal = 0
# print("Reporter Toggler 2018-01-29")

ControlSize = NSMiniControlSize # NSSmallControlSize

class ReporterToggler (PalettePlugin):
	stackView = objc.IBOutlet()
	view = objc.IBOutlet()
	
	@objc.python_method
	def settings(self):
		try:
			#NSBundle.loadNibNamed_owner_('View', self)
			self.name = 'Reporters'
			
			width = 160
			self.reporterArray = list(Glyphs.reporters)
			self.reporterArray = sorted(self.reporterArray, key=lambda reporter: reporter.title())
			self.checkboxes = []
			for i, reporter in enumerate(self.reporterArray): # Glyphs.activeReporters
				# print(reporter.classCode())
				
				frame = NSMakeRect(0, 0, 18, 18)
				checkBox = NSButton.alloc().initWithFrame_(frame)
				checkBox.setTitle_(reporter.title())
				checkBox.setButtonType_(NSSwitchButton)
				checkBox.setTarget_(self)
				checkBox.setAction_(self.toggle_)
				if reporter in Glyphs.activeReporters:
					isActive = NSOnState
				else:
					isActive = NSOffState
				checkBox.setState_(isActive)
				checkBox.setControlSize_(ControlSize)
				font = NSFont.systemFontOfSize_(NSFont.systemFontSizeForControlSize_(ControlSize))
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
			print(traceback.format_exc())

	@objc.python_method
	def start(self):
		# Adding a callback for when the visiblity of a reporter changes
		NSUserDefaults.standardUserDefaults().addObserver_forKeyPath_options_context_(self, "visibleReporters", 0, None)

	def observeValueForKeyPath_ofObject_change_context_(self, keyPath, aObject, change, context):
		self.update(self)

	def toggle_(self, sender=None):
		try:
			thisReporter = sender.title()
			for i, reporter in enumerate(self.reporterArray):
				if reporter.title() == thisReporter:
					if sender.state() == NSOffState:
						Glyphs.deactivateReporter(reporter)
					else:
						Glyphs.activateReporter(reporter)
		except:
			print(traceback.format_exc())

	@objc.python_method
	def update(self, sender=None):
		try:
			for i, reporter in enumerate(self.reporterArray): # Glyphs.activeReporters
				if reporter in Glyphs.activeReporters:
					isActive = NSOnState
				else:
					isActive = NSOffState
				self.checkboxes[i].setState_(isActive)
		except:
			print(traceback.format_exc())
	
	@objc.python_method
	def __del__(self):
		# Delete callbacks when the window is closed, otherwise it'll crash :( 
		NSUserDefaults.standardUserDefaults().removeObserver_forKeyPath_(self, "visibleReporters")
	
	def setSortID_(self, id):
		pass
	
	def sortID(self):
		return 0
