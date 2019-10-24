'''
This class returns the hardcoded static beacons (for now)
'''

class StaticBeacons():

    def build(self,df):
        static = ["0C:F3:EE:09:3A:01", "0C:F3:EE:09:38:3C", "0C:F3:EE:09:39:55",
            "0C:F3:EE:09:36:47", "0C:F3:EE:09:39:A4", "0C:F3:EE:09:38:EF",
            "0C:F3:EE:09:35:E0", "20:91:48:DF:2D:09", "20:91:48:DF:06:B1",
            "20:91:48:DE:EA:4B", "FD:3C:04:B6:A8:18", "DA:29:71:A1:D4:97",
            "20:91:48:DE:E5:6E", "2C:31:21:5C:3F:78","0C:F3:EE:09:3A:01",
            "0C:F3:EE:09:3A:11", "0C:F3:EE:09:39:A4", "0C:F3:EE:09:36:47" ,
            "20:91:48:DF:02:5F" ]
        return [s for s in static if s in df]
