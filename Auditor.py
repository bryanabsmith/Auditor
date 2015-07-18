#!/usr/bin/python

import ipgetter
import os
import platform
import subprocess
import time
import wx

# TODO Clean up the code.


# Licenced under the MIT Licence. See LICENCE for more details.

class Auditor(wx.Frame):
    def __init__(self, parent, title):

        self.audit = ""
        self.version = "0.1 (b2)"

        self.serial = True

        self.run_allChecked = False
        self.wildcardSave = "Text document (*.txt)|*.txt"

        # http://zetcode.com/wxpython/layout/
        super(Auditor, self).__init__(parent, title=title, size=(350, 300), style=wx.MINIMIZE_BOX | wx.CLOSE_BOX)

        self.panelMain = wx.Panel(self)
        self.vBoxMain = wx.BoxSizer(wx.VERTICAL)
        self.labelSelect = wx.StaticText(self.panelMain, label="Select the information that you'd like collected:")
        self.vBoxOptions = wx.BoxSizer(wx.VERTICAL)
        self.checkBoxOpen = wx.CheckBox(self.panelMain, label="Open report when done")
        self.checkBoxForumOptimized = wx.CheckBox(self.panelMain, label="Optimize for forums (BBCode)")
        self.buttonrun_all = wx.Button(self.panelMain, label="All", size=(120, 30))
        self.buttonrun_selected = wx.Button(self.panelMain, label="Selected", size=(120, 30))
        self.checkListBoxAudits = wx.CheckListBox(self.panelMain, -1,
                                                  choices=["Basic", "Networking", "Platform", "Power", "Usage"])
        self.hBoxButtons = wx.BoxSizer(wx.HORIZONTAL)

        self.sbOptions = wx.StaticBox(self.panelMain, label="Options")
        self.sbOptionsBox = wx.StaticBoxSizer(self.sbOptions, wx.VERTICAL)

        self.menuBarMain = wx.MenuBar()
        self.menuRun = wx.Menu()
        self.menuTemplates = wx.Menu()
        self.menuHelp = wx.Menu()
        self.dialogSave = wx.FileDialog(None, message="Save report as ...",
                                        defaultDir=os.path.expanduser("~") + "/Desktop/", defaultFile="",
                                        wildcard=self.wildcardSave, style=wx.SAVE)

        self.init_ui()
        self.Centre()
        self.Show()

    def init_ui(self):
        self.vBoxMain.Add(self.labelSelect, proportion=0, flag=wx.LEFT | wx.TOP, border=10)

        self.vBoxMain.Add(self.checkListBoxAudits, proportion=1, flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND,
                          border=10)
        self.sbOptionsBox.Add(self.checkBoxForumOptimized, proportion=0, flag=wx.LEFT)
        self.sbOptionsBox.Add(self.checkBoxOpen, proportion=0, flag=wx.LEFT)
        self.vBoxMain.Add(self.sbOptionsBox, proportion=0, flag=wx.LEFT | wx.RIGHT | wx.TOP | wx.EXPAND, border=10)

        self.hBoxButtons = wx.BoxSizer(wx.HORIZONTAL)
        self.hBoxButtons.Add(self.buttonrun_selected, proportion=0, flag=wx.RIGHT, border=10)
        self.hBoxButtons.Add(self.buttonrun_all, proportion=0, flag=wx.RIGHT, border=10)
        self.vBoxMain.Add(self.hBoxButtons, flag=wx.ALIGN_RIGHT | wx.BOTTOM, border=10)
        self.panelMain.SetSizer(self.vBoxMain)

        self.menuRun.Append(101, "Run all...\tCtrl-A")
        self.menuRun.Append(102, "Run selected...\tCtrl-S")

        self.menuTemplates.Append(201, "Mac-Forums essentials\tCtrl-M")

        self.menuHelp.Append(wx.ID_ABOUT, "&About Auditor")
        self.menuHelp.Append(301, "About data collected...\tCtrl-H")

        self.menuBarMain.Append(self.menuRun, "&Run")
        self.menuBarMain.Append(self.menuTemplates, "&Templates")
        self.menuBarMain.Append(self.menuHelp, "&Help")

        self.SetMenuBar(self.menuBarMain)
        self.Bind(wx.EVT_MENU, self.about_menu_click, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.run_all, id=101)
        self.Bind(wx.EVT_MENU, self.run_selected, id=102)
        self.Bind(wx.EVT_MENU, self.template_mfessentials, id=201)
        self.Bind(wx.EVT_MENU, self.show_help, id=301)
        self.Bind(wx.EVT_BUTTON, self.run_all, self.buttonrun_all)
        self.Bind(wx.EVT_BUTTON, self.run_selected, self.buttonrun_selected)

    def template_mfessentials(self, event):
        self.checkListBoxAudits.SetCheckedStrings(["Basic", "Platform", "Usage"])
        self.checkBoxForumOptimized.SetValue(True)
        self.serial = False

    def show_help(self, event):
        message = """
Here is a list of all the pieces of information collected:

- Basic:
    - OS X Version
    - OS X Build
    - Processor Info
    - Memory Info
    - Model Name
    - Model ID
    - Serial number

- Platform Info
    - Platform
    - Node
    - Release
    - Version
    - Machine
    - Processor

- Usage
    - Memory Usage: Used Memory, Wired Memory, Unused Memory
    - Hard Disk Usage, Mounted at /: Total Space, Used Space, Available Space

- Networking
    - SSID
    - Link Auth
    - IP Addresses: en0, en1
    - External IP
    - External Host
    - Ethernet DNS
    - Wi-Fi DNS

- Power
    - Battery Cycle Count
    - Battery Condition
"""

        dlg = wx.MessageDialog(self.panelMain, message, "Output", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def run_all_or_not(self, event):
        if self.checkBoxAll.GetValue():
            self.run_allChecked = True
            self.checkListBoxAudits.Disable()
        else:
            self.run_allChecked = False
            self.checkListBoxAudits.Enable()

    def about_menu_click(self, event):
        about_options = wx.AboutDialogInfo()
        about_options.SetName("Auditor")
        about_options.SetVersion(self.version)
        about_options.SetCopyright("(c) 2015 Bryan Smith.\n\nIcon courtesy of the Tango Project.\n\nExternal IP library, ipgetter, licenced under the DWTFYWT licence (http://www.wtfpl.net/)")
        aboutBox = wx.AboutBox(about_options)
        print(aboutBox)

    def button_run_audit_click(self, event):
        check = self.checkListBoxAudits.GetCheckedStrings()
        if self.run_allChecked == False and len(check) == 0:
            dialogNoChecks = wx.MessageDialog(self, "No options selected.", "Auditor",
                                              wx.OK | wx.ICON_NONE)  # | wx.ICON_INFORMATION
            dialogNoChecks.ShowModal()
            dialogNoChecks.Destroy()
        else:
            if self.run_allChecked:
                self.run_all()
            else:
                self.run_selected()

    def run_all(self, event):
        if self.checkBoxForumOptimized.GetValue() == True:
            self.audit = "[code]\nAuditor Report\n"
        else:
            self.audit = "Auditor Report\n"

        # http://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/
        self.audit += time.strftime("%d/%m/%Y, %H:%M:%S")

        progValue = 1

        # java2s.com/Tutorial/Python/0380__wxPython/Aprogressbox.htm
        dialog = wx.ProgressDialog("Collection Progress", "Starting...", 5, style=wx.PD_CAN_ABORT | wx.PD_AUTO_HIDE | wx.PD_SMOOTH)
        dialog.Pulse()

        self.get_basic()
        dialog.Update(progValue, "Getting basic information...")
        progValue += 1

        self.get_platform()
        dialog.Update(progValue, "Getting platform information...")
        progValue += 1

        self.get_usage()
        dialog.Update(progValue, "Getting usage information...")
        progValue += 1

        self.get_networking()
        dialog.Update(progValue, "Getting networking information...")
        progValue += 1

        self.get_power()
        dialog.Update(progValue, "Getting power information...")

        if self.checkBoxForumOptimized.GetValue():
            self.audit += "\n[/code]"

        path = ""
        self.dialogSave.SetFilename("Auditor-" + time.strftime("%d-%m-%Y-at-%H-%M-%S"))
        if self.dialogSave.ShowModal() == wx.ID_OK:
            path = self.dialogSave.GetPath()
            output = open(path, "w")
            output.write(self.audit)
            output.close()
            if self.checkBoxOpen.GetValue():
                subprocess.Popen(('open', path), stdout=subprocess.PIPE)

        self.checkListBoxAudits.Enable()

        self.serial = True

    def run_selected(self, event):
        check = self.checkListBoxAudits.GetCheckedStrings()
        checkLen = len(check)
        progValue = 1

        if checkLen == 0:
            dlg = wx.MessageDialog(self.panelMain, "Please select some options or run all audits.", "Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return 0

        if self.checkBoxForumOptimized.GetValue() == True:
            self.audit = "[code]\nAuditor Report\n"
        else:
            self.audit = "Auditor Report\n"

        # http://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/
        self.audit += time.strftime("%d/%m/%Y, %H:%M:%S")

        dialog = wx.ProgressDialog("Collection Progress", "Starting...", checkLen, style=wx.PD_CAN_ABORT | wx.PD_AUTO_HIDE | wx.PD_SMOOTH)
        dialog.Pulse()

        for x in check:
            if x == "Basic":
                self.get_basic()
                dialog.Update(progValue, "Getting basic information...")
                progValue += 1
            elif x == "Platform":
                self.get_platform()
                dialog.Update(progValue, "Getting platform information...")
                progValue += 1
            elif x == "Usage":
                self.get_usage()
                dialog.Update(progValue, "Getting usage information...")
                progValue += 1
            elif x == "Networking":
                self.get_networking()
                dialog.Update(progValue, "Getting networking information...")
                progValue += 1
            elif x == "Power":
                self.get_power()
                dialog.Update(progValue, "Getting power information...")
                progValue += 1


        if self.checkBoxForumOptimized.GetValue() == True:
            self.audit += "\n[/code]"

        dialog.Destroy()

        path = ""
        self.dialogSave.SetFilename("Auditor-" + time.strftime("%d-%m-%Y-at-%H-%M-%S"))
        if self.dialogSave.ShowModal() == wx.ID_OK:
            path = self.dialogSave.GetPath()
            output = open(path, "w")
            output.write(self.audit)
            output.close()
            if self.checkBoxOpen.GetValue():
                subprocess.Popen(('open', path), stdout=subprocess.PIPE)

        self.checkListBoxAudits.Enable()
        self.serial = True

    def get_basic(self):

        self.audit += "\n\n:: Basic Info ::\n"

        # http://stackoverflow.com/a/13332300
        sysctlProc = subprocess.Popen(('sysctl', '-a'), stdout=subprocess.PIPE)
        sysctlProcPipe = subprocess.check_output(('grep', 'machdep.cpu.brand_string'), stdin=sysctlProc.stdout)

        sysctlMem = subprocess.Popen(('sysctl', '-a'), stdout=subprocess.PIPE)
        sysctlMemPipe = subprocess.check_output(('grep', 'hw.memsize'), stdin=sysctlMem.stdout)

        self.audit += "     OS X Version: " + subprocess.check_output(["sw_vers", "-productVersion"])
        self.audit += "     OS X Build: " + subprocess.check_output(["sw_vers", "-buildVersion"])
        self.audit += "     Processor Info: " + sysctlProcPipe[26:]

        memMB = (int(sysctlMemPipe[12:]) / 1024) / 1024
        memGB = ((int(sysctlMemPipe[12:]) / 1024) / 1024) / 1024
        self.audit += "     Memory Info: " + str(memGB) + "GB (" + str(memMB) + "MB)"

        self.audit += "\n     Model Name: "
        modelName = subprocess.Popen(('system_profiler', 'SPHardwareDataType'), stdout=subprocess.PIPE)
        modelNamePipe = subprocess.check_output(('grep', 'Model Name'), stdin=modelName.stdout)
        for x in modelNamePipe.split():
            if x == "Model" or x == "Name:":
                pass
            else:
                self.audit += x + " "

        modelID = subprocess.Popen(('system_profiler', 'SPHardwareDataType'), stdout=subprocess.PIPE)
        modelIDPipe = subprocess.check_output(('grep', 'Identifier'), stdin=modelID.stdout)
        self.audit += "\n     Model ID: " + modelIDPipe.split()[2]

        if self.serial == True:
            serialNumber = subprocess.Popen(('system_profiler', 'SPHardwareDataType'), stdout=subprocess.PIPE)
            serialNumberPipe = subprocess.check_output(('grep', 'Serial'), stdin=serialNumber.stdout)
            self.audit += "\n     Serial number: " + serialNumberPipe.split()[3]

        # Model name - http://apple.stackexchange.com/a/98089 (curl http://support-sp.apple.com/sp/product?cc=DTY3)

    def get_power(self):

        self.audit += "\n\n:: Power Info ::\n"

        cycleCount = subprocess.Popen(('system_profiler', 'SPPowerDataType'), stdout=subprocess.PIPE)
        cycleCountPipe = subprocess.check_output(('grep', 'Cycle Count'), stdin=cycleCount.stdout)
        self.audit += "     Battery Cycle Count: " + cycleCountPipe.split()[2]

        condition = subprocess.Popen(('system_profiler', 'SPPowerDataType'), stdout=subprocess.PIPE)
        conditionPipe = subprocess.check_output(('grep', 'Condition'), stdin=condition.stdout)
        self.audit += "\n     Battery Condition: " + conditionPipe.split()[1]

    def get_platform(self):

        self.audit += "\n\n:: Platform Info ::\n"

        # http://pymotw.com/2/platform/
        self.audit += "     Platform: " + platform.system()
        self.audit += "\n     Node: " + platform.node()
        self.audit += "\n     Release: " + platform.release()
        self.audit += "\n     Version: " + platform.version()
        self.audit += "\n     Machine: " + platform.machine()
        self.audit += "\n     Processor: " + platform.processor()

    def get_usage(self):

        self.audit += "\n\n:: Usage Info ::\n"

        # http://stackoverflow.com/questions/21162721/how-to-get-physical-memory-from-top-l1-using-awk-in-os-x-mavericks - physical memory
        usedMem = subprocess.Popen(('top', '-l1'), stdout=subprocess.PIPE)
        usedMemPipe = subprocess.check_output(('grep', 'PhysMem'), stdin=usedMem.stdout)
        usedMemUsed = usedMemPipe.split()[1]
        usedMemWired = usedMemPipe.split()[3]
        usedMemUnused = usedMemPipe.split()[5]
        self.audit += "     Memory Usage:\n          Used Memory: " + usedMemUsed + "\n          Wired Memory: " + usedMemWired.replace(
            "(", "") + "\n          Unused Memory: " + usedMemUnused

        diskSpace = subprocess.Popen(["df", "-H", "/"], stdout=subprocess.PIPE)
        diskSpaceInfo = diskSpace.communicate()[0]
        totalSpace = diskSpaceInfo.split()[11]
        usedSpace = diskSpaceInfo.split()[12]
        availableSpace = diskSpaceInfo.split()[13]
        self.audit += "\n     Hard Disk Usage, Mounted at /:\n          Total Space: " + totalSpace + "\n          Used Space: " + usedSpace + "\n          Available Space: " + availableSpace

    def get_networking(self):
        # Timing:
        #   - 0.1b1: 23s
        #   - 0.1b2:

        self.audit += "\n\n:: Networking Info ::\n"

        try:
            # /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | grep SSID
            ssid = subprocess.Popen(
                ('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'),
                stdout=subprocess.PIPE)
            ssidPipe = subprocess.check_output(('grep', 'SSID'), stdin=ssid.stdout)
            self.audit += "     SSID: " + ssidPipe.split()[3]
        except subprocess.CalledProcessError:
            self.audit += "     SSID: N/A"

        # try:
            # linkAuth = subprocess.Popen(('/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'), stdout=subprocess.PIPE)
            # linkAuthPipe = subprocess.check_output(('grep', 'link'), stdin=linkAuth.stdout)
            # self.audit += "\n     Link Auth: " + linkAuthPipe.split()[2]
        # except subprocess.CalledProcessError:
            # self.audit += "\n     Link Auth: N/A"

        ipEN0 = subprocess.Popen(["ipconfig", "getifaddr", "en0"], stdout=subprocess.PIPE)
        ipEN0Value = ipEN0.communicate()[0].strip("\n")
        if ipEN0Value == "":
            self.audit += "\n     IP Addresses:\n          en0: N/A"
        else:
            self.audit += "\n     IP Addresses:\n          en0: " + ipEN0Value
        print(ipEN0Value)

        ipEN1 = subprocess.Popen(["ipconfig", "getifaddr", "en1"], stdout=subprocess.PIPE)
        ipEN1Value = ipEN1.communicate()[0].strip("\n")
        if ipEN1Value == "":
            self.audit += "\n          en1: N/A"
        else:
            self.audit += "\n          en1: " + ipEN1Value
        print(ipEN1Value)

        # extIP = subprocess.Popen(["curl", "ifconfig.me"], stdout=subprocess.PIPE)
        extIP = ipgetter.myip()
        self.audit += "\n          External IP: " + extIP

        # extHost = subprocess.Popen(["curl", "ifconfig.me/host"], stdout=subprocess.PIPE)
        # self.audit += "          External Host: " + extHost.communicate()[0]

        ethernetDNS = subprocess.Popen(["networksetup", "-getdnsservers", "Ethernet"], stdout=subprocess.PIPE)
        self.audit += "\n          Ethernet DNS: " + ethernetDNS.communicate()[0].replace("\n", "  ")

        wifiDNS = subprocess.Popen(["networksetup", "-getdnsservers", "Wi-Fi"], stdout=subprocess.PIPE)
        self.audit += "\n          Wi-Fi DNS: " + wifiDNS.communicate()[0].replace("\n", "  ")

if __name__ == "__main__":
    app = wx.App()
    Auditor(None, title="Auditor")
    app.MainLoop()