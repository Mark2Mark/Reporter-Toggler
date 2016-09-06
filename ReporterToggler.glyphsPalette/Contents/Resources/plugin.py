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
import traceback

class ReporterToggler (PalettePlugin):

	def settings(self):
		try:
			self.name = 'Reporters'
			# Vanilla window and group with controls
			width = 160 # 150
			elementHeight = 15 # 15
			height = len(Glyphs.reporters) * elementHeight # 900
			self.paletteView = Window((width, height + 10))
			self.paletteView.group = Group((0, 0, width, height + 10))
			# self.paletteView.group.text = TextBox((10, 0, -10, -10), self.name, sizeStyle='small')
			reporterArray = [u"%s" % r.title() for r in Glyphs.reporters]
			# reporterArraySorted = sorted(reporterArray)


			# for i, reporter in enumerate(reporterArraySorted): # Glyphs.activeReporters
			for i, reporter in enumerate(reporterArray): # Glyphs.activeReporters
				if reporter in Glyphs.activeReporters:
					isActive = True
				else:
					isActive = False
				attrName = "CheckBox_%s" % str(i)
				checkBox = CheckBox( (10, elementHeight*i, -10, elementHeight), reporter.title(), sizeStyle='small', value=isActive, callback=self.toggle )
				setattr(self.paletteView.group, attrName, checkBox)

			# Set dialog to NSView
			self.dialog = self.paletteView.group.getNSView()
		except:
			self.logToConsole(traceback.format_exc())

	def start(self):
		# Adding a callback for the 'GSUpdateInterface' event
		s = objc.selector( self.update, signature="v@:" )
		NSNotificationCenter.defaultCenter().addObserver_selector_name_object_( self, s, "GSUpdateInterface", None )  # GSDocumentCloseNotification | GSDocumentActivateNotification

	def toggle(self, sender):
		try:
			thisReporter = sender.getTitle()
			for rep in Glyphs.reporters:
				if rep.title() == thisReporter:
					if sender.get() == 0:
						print "off", thisReporter, rep.title()
						Glyphs.deactivateReporter(rep)
					if sender.get() == 1:
						print "on", thisReporter
						Glyphs.activateReporter(rep)
		except:
			print traceback.format_exc()


	def update( self, sender ):
		try:
			for i, reporter in enumerate(Glyphs.reporters): # Glyphs.activeReporters
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

