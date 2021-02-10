import gi
import subprocess

gi.require_version("Gtk","3.0")
from gi.repository import Gtk

def getDeviceCodename():
    result = subprocess.run(['adb', 'shell', 'getprop', 'ro.product.vendor.device'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    return result.strip()

class PaInstaller(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Paranoid Installer")
        self.set_border_width(10)
        hbox = Gtk.Box(spacing=6)
        hbox.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(hbox)
        self.aboutDevice = Gtk.Button(label='Check Connected Device')
        self.aboutDevice.connect("clicked", self.on_about_device)
        hbox.pack_start(self.aboutDevice, True, True, 0)
        self.recoveryreboot = Gtk.Button(label='Reboot to Recovery')
        self.recoveryreboot.connect("clicked", self.on_recovery_reboot)
        hbox.pack_start(self.recoveryreboot, True, True, 0)
        self.fastbootreboot = Gtk.Button(label='Reboot to Fastboot')        
        self.fastbootreboot.connect("clicked", self.on_pa_click)
        hbox.pack_start(self.fastbootreboot, True, True, 0)

    def on_about_device(self, widget):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Connected device",
        )
        dialog.format_secondary_text(
            "Connected device: "+getDeviceCodename()
        )
        dialog.run()
        print("Task dialog closed")

        dialog.destroy()

    def Finished(self, widget):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Task completed successfully",
        )
        dialog.format_secondary_text(
            "The given task completed successfully."
        )
        dialog.run()
        print("Task dialog closed")

        dialog.destroy()

    def on_pa_click(self, widget):
        subprocess.run(['adb', 'reboot', 'bootloader'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        dialog = self.Finished(self)

    def on_recovery_reboot(self, widget):
        subprocess.run(['adb', 'reboot', 'recovery'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        dialog = self.Finished(self)

win = PaInstaller()
win.connect("destroy",Gtk.main_quit)

win.show_all()
Gtk.main()
