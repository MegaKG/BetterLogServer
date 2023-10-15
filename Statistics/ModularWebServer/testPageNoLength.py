#GNU General Public License v3.0
#Code by MegaKG
import Pages


print("Some Initialisation code can go here")

#Refer to Pages
class page(Pages.webpage):
    def connect(self):
        self.sendCode('200 OK')
        self.sendType("text/html")

        self.print("<html>Hello World - No Length</html>")
        self.close()
