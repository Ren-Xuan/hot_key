
import win32gui
import win32api
import ctypes
import win32con
import win32ui
import numpy as np
class GameAssist:

    def __init__(self, wdname):
        """初始化"""
        # 取得窗口句柄
        self.hwnd = win32gui.FindWindow(0, wdname)
        if not self.hwnd:
            print("window does not exit")
            exit()
        """
        GetWindowRect() 得到的是在屏幕坐标系下的RECT；（即以屏幕左上角为原点） 
        GetClientRect() 得到的是在客户区坐标系下的RECT； （即以所在窗口左上角为原点）
        GetWindowRect()取的是整个窗口的矩形； 
        GetClientRect()取的仅是客户区的矩形，也就是说不包括标题栏，外框等.
        
        """
        self.rePos()
        self.pos = self.getPos()
        x1,y1,x2,y2 =self.pos
        self.w = x2-x1
        self.h = y2-y1
        print("find the position:" + str(self.pos))
        print("ennd")

    def getPos(self):
        return win32gui.GetWindowRect(self.hwnd)
    def rePos(self):
        """
        z-order 为 HWND_TOPMOST（也就是所有非顶层窗口的最上面）
        z-order 为 HWND_TOP（也就是最顶层窗口）
        """
        win32gui.SetWindowPos(self.hwnd,win32con.HWND_TOP,0,0,0,0,win32con.SWP_NOSIZE)
    def start():
        #while True:
        """
        点击
        查看值
        if 值>目标：
            购买动作
        wait 热键
        """
        pass
    def click(self,x,y):            
        ctypes.windll.user32.SetCursorPos(x,y)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0 ,0, 0, 0)
        print("ennd")
    def move(self,x,y):
        ctypes.windll.user32.SetCursorPos(x,y)


    def init_mem(self , w = -1 ,h = -1):
        self.hwindc = win32gui.GetWindowDC(self.hwnd)
        self.srcdc = win32ui.CreateDCFromHandle(self.hwindc)
        self.memdc = self.srcdc.CreateCompatibleDC()
        self.bmp = win32ui.CreateBitmap()
        if w == -1:
            self.bmp.CreateCompatibleBitmap(self.srcdc, self.w,self.h)
        else:
            self.bmp.CreateCompatibleBitmap(self.srcdc, w,h)
        self.memdc.SelectObject(self.bmp)
            
    def clean_mem(self):
        self.srcdc.DeleteDC()
        self.memdc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.hwindc)
        win32gui.DeleteObject(self.bmp.GetHandle())

    def window_full_shot(self, file_name=None, gray=0):
        """
        窗口截图
            :param file_name=None: 截图文件的保存名称
            :param gray=0: 是否返回灰度图像，0：返回BGR彩色图像，其他：返回灰度黑白图像
            :return: file_name为空则返回RGB数据
        """
        pos = self.getPos()
        return self.window_part_shot((pos[0],pos[1]),(pos[2],pos[3]),file_name,gray)

    def window_part_shot(self, pos1, pos2, file_name=None, gray=0):
        """
        窗口区域截图
            :param pos1: (x,y) 截图区域的左上角坐标
            :param pos2: (x,y) 截图区域的右下角坐标
            :param file_name=None: 截图文件的保存路径
            :param gray=0: 是否返回灰度图像，0：返回BGR彩色图像，其他：返回灰度黑白图像
            :return: file_name为空则返回RGB数据
        """
        w = pos2[0]-pos1[0]
        h = pos2[1]-pos1[1]
        self.init_mem(w,h)
        """
            BOOLBitBlt(int x,int y,int nWidth,int nHeight,CDC*pSrcDC,int xSrc,int ySrc,DWORDdwRop);
            x：目标矩形区域的左上角x轴坐标点。
            y：目标矩形区域的左上角y轴坐标点。
            nWidth：在目标设备中绘制位图的宽度。
            nHight：在目标设备中绘制位图的高度。
            pSrcDC：源设备上下文对象指针。
            xSrc：源设备上下文的起点x轴坐标，函数从该起点复制位图到目标设备。
            ySrc：源设备上下文的起点y轴坐标，函数从该起点复制位图到目标设备。
            dwRop：光栅操作代码
            """
        self.memdc.BitBlt(pos1, (w, h), self.srcdc,(0,0), win32con.SRCCOPY)
        if file_name != None:
            self.bmp.SaveBitmapFile(self.memdc, file_name)
            self.clean_mem()
            return
        else:
            signedIntsArray = self.bmp.GetBitmapBits(True)
            img = np.fromstring(signedIntsArray, dtype='uint8')
            img.shape = (h, w, 4)
            self.clean_mem()
            if gray == 0:
                return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            else:
                return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    def check_color(self, pos, color, tolerance=0):
        """
        对比窗口内某一点的颜色
            :param pos: (x,y) 欲对比的坐标
            :param color: (r,g,b) 欲对比的颜色 
            :param tolerance=0: 容差值
            :return: 成功返回True,失败返回False
        """
        img = Image.fromarray(self.window_full_shot(), 'RGB')
        r1, g1, b1 = color[:3]
        r2, g2, b2 = img.getpixel(pos)[:3]
        if abs(r1-r2) <= tolerance and abs(g1-g2) <= tolerance and abs(b1-b2) <= tolerance:
            return True
        else:
            return False
    def find_img(self, img_template_path, part=0, pos1=None, pos2=None, gray=0):
        """
        查找图片
            :param img_template_path: 欲查找的图片路径
            :param part=0: 是否全屏查找，1为否，其他为是
            :param pos1=None: 欲查找范围的左上角坐标
            :param pos2=None: 欲查找范围的右下角坐标
            :param gray=0: 是否彩色查找，0：查找彩色图片，1：查找黑白图片
            :return: (maxVal,maxLoc) maxVal为相关性，越接近1越好，maxLoc为得到的坐标
        """
        # 获取截图
        if part == 1:
            img_src = self.window_part_shot(pos1, pos2, None, gray)
        else:
            img_src = self.window_full_shot(None, gray)

        # show_img(img_src)

        # 读入文件
        if gray == 0:
            img_template = cv2.imread(img_template_path, cv2.IMREAD_COLOR)
        else:
            img_template = cv2.imread(img_template_path, cv2.IMREAD_GRAYSCALE)

        try:
            res = cv2.matchTemplate(
                img_src, img_template, cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
            # print(maxLoc)
            return maxVal, maxLoc
        except Exception:
            logging.warning('find_img执行失败')
            a = traceback.format_exc()
            logging.warning(a)
            return 0, 0
    def find_img_knn(self, img_template_path, part=0, pos1=None, pos2=None, gray=0, thread=0):
        """
        查找图片，knn算法
            :param img_template_path: 欲查找的图片路径
            :param part=0: 是否全屏查找，1为否，其他为是
            :param pos1=None: 欲查找范围的左上角坐标
            :param pos2=None: 欲查找范围的右下角坐标
            :param gray=0: 是否彩色查找，0：查找彩色图片，1：查找黑白图片
            :return: 坐标(x, y)，未找到则返回(0, 0)，失败则返回-1
        """
        # 获取截图
        if part == 1:
            img_src = self.window_part_shot(pos1, pos2, None, gray)
        else:
            img_src = self.window_full_shot(None, gray)

        # show_img(img_src)

        # 读入文件
        if gray == 0:
            img_template = cv2.imread(img_template_path, cv2.IMREAD_COLOR)
        else:
            img_template = cv2.imread(img_template_path, cv2.IMREAD_GRAYSCALE)

        try:
            maxLoc = match_img_knn(img_template, img_src, thread)
            # print(maxLoc)
            return maxLoc
        except Exception:
            logging.warning('find_img_knn执行失败')
            a = traceback.format_exc()
            logging.warning(a)
            return -1

if __name__ == "__main__":
    # wdname窗口的名称，必须写完整
    wdname =u"任务管理器"
    demo = GameAssist(wdname)
    demo.rePos()
    pos = demo.getPos()
    demo.window_part_shot((pos[0],pos[1]),(pos[2]-pos[0],pos[3]-pos[1]),"c:/testFullPart.bmp")
    demo.window_part_shot((pos[0],pos[1]),((pos[2]-pos[0])//2,(pos[3]-pos[1])//2),"c:/testHalfPart.bmp")
    demo.window_full_shot("c:/testFull.bmp")
    pos = demo.getPos()
    print(pos)
    #demo.click(pos[2]-10,pos[1]+10)