from tkinter import *
import pymysql
from tkinter import messagebox  # 消息提示框
from tkinter import ttk


class Basedesk:
    """
    基准框模块
    """

    def __init__(self, master):
        # 主界面
        self.root = master  # 窗口传入
        self.root.config()  # 顶层菜单
        self.root.title('学生成绩管理系统')
        self.width = 600  # 界面宽
        self.height = 300  # 界面高
        # 获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
        self.screenwidth = self.root.winfo_screenwidth()  # 屏幕宽
        self.screenheight = self.root.winfo_screenheight()  # 屏幕高
        self.alignstr = '%dx%d+%d+%d' % (
            self.width, self.height, (self.screenwidth - self.width) / 2, (self.screenheight - self.height) / 2)
        self.root.geometry(self.alignstr)

        # 进入应用
        self.R = Register(self.root)
        self.R.register()


class Register:

    def __init__(self, master):
        self.root = master  # 窗口传入
        # 数据库登录
        self.ip = 'localhost'
        self.port = 3306
        self.id = 'root'
        self.pd = 'Xyn20040516!'
        self.db = 'school_db'
        # 个人信息
        self.no = ''
        self.name = ''
        self.sex = ''
        self.birthday = ''
        self.tel = ''
        self.flag = 0
        # 临时变量(click单击后选择的变量 smanage中)
        self.temporary_sno = ''
        self.temporary_sname = ''
        self.temporary_sex = ''
        self.temporary_birth = ''
        self.temporary_tel = ''
        self.temporary_pwd = ''
        self.temporary_cno = ''
        self.temporary_cname = ''

    '''
    登录模块
    '''

    def register(self):
        # 账号密码输入框
        self.initface = LabelFrame(self.root, text='学生成绩管理系统', font=('微软雅黑', 16))
        self.initface.grid(row=1, column=0, padx=170, pady=30, )

        self.people = Label(self.initface, text='账号 :', font=('黑体', 12))  # 账号
        self.people.grid(row=1, column=0, padx=20, pady=10, sticky=W)
        self.password = Label(self.initface, text='密码 :', font=('黑体', 12))  # 密码
        self.password.grid(row=2, column=0, padx=20, pady=10, sticky=W)
        self.var1 = StringVar
        self.var2 = StringVar
        self.entry_people = Entry(self.initface, textvariable=self.var1)  # 账号输入框
        self.entry_people.grid(row=1, column=1, padx=10, pady=10)
        self.entry_password = Entry(self.initface, textvariable=self.var2, show='*')  # 密码输入框
        self.entry_password.grid(row=2, column=1, padx=10, pady=10)

        self.button_into = Button(self.initface, text='登录', command=self.conn)  # 登录按钮
        self.button_into.grid(row=3, column=0, padx=10, pady=20, sticky=E)
        self.button_into = Button(self.initface, text='退出', command=self.root.quit)  # 退出按钮
        self.button_into.grid(row=3, column=1, padx=20, pady=20, )

    # ======= register的登录
    def conn(self):
        self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
        self.cursor = self.connect.cursor()
        if self.connect:
            print('连接成功')
        user = self.entry_people.get()
        password = self.entry_password.get()

        # 学生登录验证
        self.ssql = "SELECT * FROM student_pwd WHERE user=%s AND pwd=%s"
        self.cursor.execute(self.ssql, (user, password))
        self.result = self.cursor.fetchone()
        if self.result:
            print('账号密码正确')
            self.flag = 1
            self.no = self.result[0]
            self.initface.destroy()  # 销毁initface
            self.check()
        else:
            # 教师登录验证
            self.tsql = "SELECT * FROM teacher_pwd WHERE user=%s AND pwd=%s"
            self.cursor.execute(self.tsql, (user, password))
            self.result = self.cursor.fetchone()
            if self.result:
                print('账号密码正确')
                self.flag = 2
                self.no = self.result[0]
                self.initface.destroy()  # 销毁initface
                self.check()

        # 若均未登录成功
        if self.flag == 0:
            # 账号或密码错误清空输入框
            self.entry_people.delete(0, END)
            self.entry_password.delete(0, END)
            messagebox.showinfo(title='提示', message='账号或密码输入错误\n请重新输入?')

        create_view_sql = """
            CREATE OR REPLACE VIEW student_scores_view AS
            SELECT 
                s.sno,
                s.sname,
                sc.tcid,
                sc.score
            FROM
                student s
            JOIN
                student_course sc ON s.sno = sc.sno;
            """
        self.cursor.execute(create_view_sql)
        self.connect.commit()

        self.cursor.close()
        self.connect.close()
    '''
    选择模块
    '''

    def query_course_students(self):
        def fetch_course_students():
            course_no = entry_course_no.get()

            # 连接数据库
            self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
            if self.connect:
                print('连接成功')
                print(self.no)  # 用户名, 即工号

                # 查询语句
                search_sql = "SELECT * FROM course_student_view WHERE cno = %s"

                # 创建游标
                self.cursor2 = self.connect.cursor()
                self.cursor2.execute(search_sql, (course_no,))
                self.row = self.cursor2.fetchone()  # 读取查询结果

                # 清空 treeview
                for item in self.treeview.get_children():
                    self.treeview.delete(item)

                # 插入查询结果
                while self.row:
                    self.treeview.insert('', 0,
                                         values=(self.row[0], self.row[1], self.row[2], self.row[3], self.row[4]))
                    self.row = self.cursor2.fetchone()

                self.cursor2.close()
                self.connect.close()

        # 创建查询窗口
        query_window = Tk()
        query_window.geometry('600x400+100+100')
        query_window.title('课程学生查询')

        # 输入框和按钮
        label_course_no = Label(query_window, text='课程号:', font=('黑体', 12))
        label_course_no.grid(row=0, column=0, padx=10, pady=10)
        entry_course_no = Entry(query_window)
        entry_course_no.grid(row=0, column=1, padx=10, pady=10)
        button_fetch = Button(query_window, text='查询', command=fetch_course_students)
        button_fetch.grid(row=0, column=2, padx=10, pady=10)

        # 表格框
        columns = ("课程号", "课程名", "学生号", "学生名", "成绩")
        self.treeview = ttk.Treeview(query_window, height=18, show="headings", columns=columns)
        self.treeview.column("课程号", width=100, anchor='center')
        self.treeview.column("课程名", width=150, anchor='center')
        self.treeview.column("学生号", width=100, anchor='center')
        self.treeview.column("学生名", width=150, anchor='center')
        self.treeview.column("成绩", width=100, anchor='center')

        self.treeview.heading("课程号", text="课程号")
        self.treeview.heading("课程名", text="课程名")
        self.treeview.heading("学生号", text="学生号")
        self.treeview.heading("学生名", text="学生名")
        self.treeview.heading("成绩", text="成绩")
        self.treeview.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        query_window.mainloop()

    # 登录conn之后, 进入check界面
    def check(self):
        # 查询并记录基本信息
        self.basic()  # self.no self.name self.sex self.sex self.birthday self.tel
        self.label_basic = Label(self.root, text='\n'
                                                 '学号/工号: %s\n\n'
                                                 '姓名: %s\n\n'
                                                 '性别: %s\n\n'
                                                 '出生日期: %s\n\n'
                                                 '联系方式: %s\n\n' %
                                                 (self.no, self.name, self.sex,
                                                  self.birthday, self.tel),
                                 font=('宋体', 10)
                                 )
        self.label_basic.grid(row=0, columnspan=4, padx=230)
        # 界面
        self.frame_checkbutton = LabelFrame(self.root, text='功能选择', font=('微软雅黑', 14))
        self.frame_checkbutton.grid(padx=60, pady=10)
        if self.flag == 1:
            # 查询成绩按钮
            self.button_success = Button(self.frame_checkbutton, text='查询成绩', width=10, height=2, command=self.success)
            self.button_success.grid(row=1, column=0, padx=20, pady=20)

            # 选择课程按钮
            self.button_select = Button(self.frame_checkbutton, text='选课', width=10, height=2, command=self.select)
            self.button_select.grid(row=1, column=1, padx=20, pady=20)
        elif self.flag == 2:
            # 学生管理按钮 以及成绩管理
            self.button_smanage = Button(self.frame_checkbutton, text='学生管理', width=10, height=2,
                                         command=self.smanage)
            self.button_smanage.grid(row=1, column=0, padx=20, pady=20)

            self.button_cmanage = Button(self.frame_checkbutton, text='课程管理', width=10, height=2,
                                         command=self.cmanage)
            self.button_cmanage.grid(row=1, column=1, padx=20, pady=20)

            # 添加课程学生查询按钮
            self.button_query_course_students = Button(self.frame_checkbutton, text='课程学生查询', width=15, height=2,
                                                       command=self.query_course_students)
            self.button_query_course_students.grid(row=2, column=0, padx=20, pady=20)

        # 修改密码按钮
        self.button_revise = Button(self.frame_checkbutton, text='修改密码', width=10, height=2, command=self.revise)
        self.button_revise.grid(row=1, column=2, padx=20, pady=20)
        # 修改信息按钮
        self.button_select = Button(self.frame_checkbutton, text='修改信息', width=10, height=2, command=self.update)
        self.button_select.grid(row=1, column=3, padx=20, pady=20)

    # 使用basic以记录基本信息
    def basic(self):
        # 链接数据库
        self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
        if self.connect:
            print('连接成功')
            print(self.no)  # 用户名, 即学号/工号
            # 查询语句
            search_sql = ''
            if self.flag == 1:
                search_sql = "SELECT * FROM student WHERE sno=%s"
            elif self.flag == 2:
                search_sql = "SELECT * FROM teacher WHERE tno=%s"
            # 创建游标
            self.cursor1 = self.connect.cursor()
            self.cursor1.execute(search_sql, (self.no,))
            self.row = self.cursor1.fetchone()  # 读取查询结果

            self.name = self.row[1]
            self.sex = self.row[2]
            self.birthday = self.row[3]
            self.tel = self.row[4]
            self.row = ()  # 查询结果置空

    # 查询成绩界面
    def success(self):
        # 链接数据库
        self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
        if self.connect:
            print('连接成功')
            print(self.no)  # 用户名, 即学号
            # 查询语句
            search_sql = "SELECT c.cno, c.cname, sc.score " \
                         "FROM student_course sc " \
                         "INNER JOIN course c ON sc.tcid = c.cno " \
                         "WHERE sc.sno = %s"

            # 创建游标
            self.cursor1 = self.connect.cursor()
            self.cursor1.execute(search_sql, (self.no,))
            self.row = self.cursor1.fetchone()  # 读取查询结果

            # 表格框
            root = Tk()  # 初始框的声明
            root.geometry('500x400+100+100')
            root.title('成绩查询系统')
            columns = ("姓名", "学号", "课程", "成绩")
            self.treeview = ttk.Treeview(root, height=18, show="headings", columns=columns)
            self.treeview.column("姓名", width=150, anchor='center')  # 表示列,不显示
            self.treeview.column("学号", width=100, anchor='center')
            self.treeview.column("课程", width=150, anchor='center')
            self.treeview.column("成绩", width=100, anchor='center')

            self.treeview.heading("姓名", text="姓名")  # 显示表头
            self.treeview.heading("学号", text="学号")
            self.treeview.heading("课程", text="课程")
            self.treeview.heading("成绩", text="成绩")
            self.treeview.pack(side=LEFT, fill=BOTH)

            # 插入查询结果
            while self.row:
                self.treeview.insert('', 0, values=(self.name, self.no, self.row[1], self.row[2]))
                self.row = self.cursor1.fetchone()

            self.cursor1.close()
            self.connect.close()
            root.mainloop()

    # 修改密码界面
    def revise(self):
        self.window = Tk()  # 初始框的声明
        self.window.geometry('400x200+100+100')
        self.window.title('密码修改管理')
        self.frame_revise = LabelFrame(self.window)
        self.frame_revise.grid(padx=60, pady=60)
        self.label_revise = Label(self.frame_revise, text='新密码：')
        self.label_revise.grid(row=0, column=0, padx=10, pady=10)
        self.var3 = StringVar
        self.entry_revise = Entry(self.frame_revise, textvariable=self.var3)
        self.entry_revise.grid(row=0, column=1, padx=10, pady=10)
        self.button_ok = Button(self.frame_revise, text='确定', command=self.revise_ok)
        self.button_ok.grid(row=1, column=0)
        self.button_resive = Button(self.frame_revise, text='取消', command=self.revise_resive)
        self.button_resive.grid(row=1, column=1)
        self.button_quit = Button(self.frame_revise, text='退出', command=self.window.destroy)
        self.button_quit.grid(row=1, column=2)

    # ======= revise的"确定"按钮
    def revise_ok(self):
        # 连接数据库
        self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
        self.cursor2 = self.connect.cursor()  # 创建游标
        sql_revise = ''
        new_password = self.entry_revise.get()
        if self.flag == 1:
            sql_revise = "UPDATE student_pwd SET pwd=%s WHERE user=%s"
        elif self.flag == 2:
            sql_revise = "UPDATE teacher_pwd SET pwd=%s WHERE user=%s"

        if self.connect:
            print('连接成功')
            print(self.no)
            self.cursor2.execute(sql_revise, (new_password, self.no))
            self.connect.commit()
            print(new_password)
            messagebox.showinfo(title='提示', message='密码修改成功!')
            self.cursor2.close()
            self.connect.close()

    # ======= revise的"取消"按钮
    def revise_resive(self):
        self.entry_revise.delete(0, END)

    # 选择课程界面
    def select(self):
        # 链接数据库
        self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
        if self.connect:
            print('连接成功')
            print(self.no)  # 用户名, 即学号
            # 查询语句
            search_sql1 = "SELECT * FROM course"
            search_sql2 = "SELECT c.cno, c.cname, c.credit " \
                          "FROM student_course sc " \
                          "INNER JOIN course c ON sc.tcid = c.cno " \
                          "WHERE sc.sno = %s"

            # 创建游标
            self.cursor1 = self.connect.cursor()

            # 初始框的声明
            root_select = Tk()
            root_select.geometry('700x500+100+100')
            root_select.title('选课系统')

            # 所有课程表格框
            columns = ("编号", "课程", "学分")
            self.treeview1 = ttk.Treeview(root_select, height=18, show="headings", columns=columns)
            self.treeview1.column("编号", width=50, anchor='center')  # 表示列,不显示
            self.treeview1.column("课程", width=75, anchor='center')
            self.treeview1.column("学分", width=50, anchor='center')
            self.treeview1.heading("编号", text="编号")  # 显示表头
            self.treeview1.heading("课程", text="课程")
            self.treeview1.heading("学分", text="学分")
            self.treeview1.grid(row=1, column=0, rowspan=3)
            # 插入查询结果
            self.cursor1.execute(search_sql1)
            self.row = self.cursor1.fetchone()  # 读取查询结果
            while self.row:
                self.treeview1.insert('', 0, values=(self.row[0], self.row[1], self.row[2]))
                self.row = self.cursor1.fetchone()

            # 已选课程表格框
            self.treeview2 = ttk.Treeview(root_select, height=18, show="headings", columns=columns)
            self.treeview2.column("编号", width=50, anchor='center')  # 表示列,不显示
            self.treeview2.column("课程", width=75, anchor='center')
            self.treeview2.column("学分", width=50, anchor='center')
            self.treeview2.heading("编号", text="编号")  # 显示表头
            self.treeview2.heading("课程", text="课程")
            self.treeview2.heading("学分", text="学分")
            self.treeview2.grid(row=1, column=1, rowspan=3)
            # 插入查询结果
            self.cursor1.execute(search_sql2, (self.no,))
            self.row = self.cursor1.fetchone()  # 读取查询结果
            while self.row:
                self.treeview2.insert('', 0, values=(self.row[0], self.row[1], self.row[2]))
                self.row = self.cursor1.fetchone()

            # 标签
            self.label_selectcourse1 = Label(root_select, text='学校开设课程表')
            self.label_selectcourse1.grid(row=0, column=0, padx=10, pady=10)
            self.label_selectcourse2 = Label(root_select, text='已选课程表')
            self.label_selectcourse2.grid(row=0, column=1, padx=10, pady=10)

            # 按钮框
            self.frame_selectbutton = LabelFrame(root_select, text='选课', font=('微软雅黑', 14))
            self.frame_selectbutton.grid(row=0, column=2, padx=10, pady=10, rowspan=4)
            # 输入框
            self.var4 = StringVar
            self.entry_insert = Entry(self.frame_selectbutton, textvariable=self.var4)
            self.entry_insert.grid(row=2, column=2, padx=10, pady=10)
            # 插入课程按钮
            self.button_insert = Button(self.frame_selectbutton, text='选择', width=10, height=2,
                                        command=self.select_insert)
            self.button_insert.grid(row=3, column=2, padx=10, pady=10)
            # Label
            self.label_selectcourse3 = Label(self.frame_selectbutton, text="输入要选择的课程编号: ")
            self.label_selectcourse3.grid(row=1, column=2, padx=10, pady=10)

            self.cursor1.close()
            self.connect.close()
            root_select.mainloop()

    # 修改信息界面
    def update(self):
        self.window = Tk()
        self.window.geometry('400x400')
        self.window.title('更新个人信息')

        self.varno = StringVar(self.window, value=self.no)
        self.varname = StringVar(self.window, value=self.name)
        self.varsex = StringVar(self.window, value=self.sex)
        self.varbirth = StringVar(self.window, value=self.birthday)
        self.vartel = StringVar(self.window, value=self.tel)
        # 输入框展示个人信息
        self.entry_no = Entry(self.window, textvariable=self.varno, state='disabled')  # 账号输入框
        self.entry_no.grid(row=1, column=1, padx=10, pady=10)
        self.entry_name = Entry(self.window, textvariable=self.varname)  # 名字输入框
        self.entry_name.grid(row=2, column=1, padx=10, pady=10)
        self.entry_sex = Entry(self.window, textvariable=self.varsex)  # 性别输入框
        self.entry_sex.grid(row=3, column=1, padx=10, pady=10)
        self.entry_birth = Entry(self.window, textvariable=self.varbirth)  # birth输入框
        self.entry_birth.grid(row=4, column=1, padx=10, pady=10)
        self.entry_tel = Entry(self.window, textvariable=self.vartel)
        self.entry_tel.grid(row=5, column=1, padx=10, pady=10)
        # Label输入框
        self.label_no = Label(self.window, text='学号/工号:', font=('黑体', 12))
        self.label_no.grid(row=1, column=0, padx=10, pady=10)
        self.label_name = Label(self.window, text='姓名:', font=('黑体', 12))
        self.label_name.grid(row=2, column=0, padx=10, pady=10)
        self.label_sex = Label(self.window, text='性别:', font=('黑体', 12))
        self.label_sex.grid(row=3, column=0, padx=10, pady=10)
        self.label_birth = Label(self.window, text='生日:', font=('黑体', 12))
        self.label_birth.grid(row=4, column=0, padx=10, pady=10)
        self.label_tel = Label(self.window, text='联系方式:', font=('黑体', 12))
        self.label_tel.grid(row=5, column=0, padx=10, pady=10)
        # Lable个人信息
        self.label_info = Label(self.window, text='\n'
                                                  '学号/工号: %s\n\n'
                                                  '姓名: %s\n\n'
                                                  '性别: %s\n\n'
                                                  '出生日期: %s\n\n'
                                                  '联系方式: %s\n\n' %
                                                  (self.no, self.name, self.sex,
                                                   self.birthday, self.tel),
                                font=('宋体', 10)
                                )
        self.label_info.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky=W)
        # 更新按钮
        self.button_update = Button(self.window, text='更新', width=10, height=2, command=self.update_up)
        self.button_update.grid(row=2, column=2, padx=10, pady=10, rowspan=3)

        self.window.mainloop()

    # ======= select的"选课"按钮
    def select_insert(self):
        # 连接数据库
        self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
        self.cursor2 = self.connect.cursor()  # 创建游标
        # 查询输入课程是否存在
        sql_insert1 = "SELECT * FROM course WHERE cno = %s"
        course_number = self.entry_insert.get()
        # 插入/忽略课程
        sql_insert2 = "INSERT IGNORE INTO student_course (sno, tcid) VALUES (%s, %s);"

        try:
            self.cursor2.execute(sql_insert1, (course_number,))
            self.result = self.cursor2.fetchone()
            if self.result:
                self.cursor2.execute(sql_insert2, (self.no, course_number))
                self.connect.commit()
                messagebox.showinfo(title='提示', message='已添加/已存在!')
            else:
                messagebox.showinfo(title='提示', message='请输入正确的课程编号!')
        except pymysql.Error as e:
            messagebox.showinfo(title='数据库错误', message=str(e))
        finally:
            self.cursor2.close()
            self.connect.close()

    # ======= update的"修改信息"按钮
    def update_up(self):
        # 连接数据库
        self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
        self.cursor2 = self.connect.cursor()  # 创建游标
        sql_up = ''
        if self.flag == 1:
            sql_up = "UPDATE student SET sname=%s, sex=%s, birthday=%s, tel=%s WHERE sno=%s"
        elif self.flag == 2:
            sql_up = "UPDATE teacher SET tname=%s, sex=%s, birthday=%s, tel=%s WHERE tno=%s"

        if self.connect:
            print('连接成功')
            print(self.no)
            self.cursor2.execute(sql_up, (self.entry_name.get(), self.entry_sex.get(), self.entry_birth.get(), self.entry_tel.get(), self.no))
            self.connect.commit()
            messagebox.showinfo(title='提示', message='信息修改成功!')
            self.cursor2.close()
            self.connect.close()

    # 学生管理界面
    def smanage(self):
        # 链接数据库
        self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
        if self.connect:
            print('连接成功')
            print(self.no)  # 用户名, 即学号
            # 查询语句
            search_sql1 = "SELECT sno, sname, sex, birthday, tel, pwd " \
                          "FROM student " \
                          "INNER JOIN student_pwd ON sno = user"

            # 创建游标
            self.cursor2 = self.connect.cursor()

            # 初始框的声明
            root_smanage = Tk()
            root_smanage.geometry("1150x550+100+100")
            root_smanage.title("学生管理系统")

            # 学生管理表格框
            columns = ("学号", "姓名", "性别", "生日", "电话", "密码")
            self.treeview3 = ttk.Treeview(root_smanage, height=18, show="headings", columns=columns)
            self.treeview3.column("学号", width=80, anchor='center')  # 表示列,不显示
            self.treeview3.column("姓名", width=70, anchor='center')
            self.treeview3.column("性别", width=50, anchor='center')
            self.treeview3.column("生日", width=100, anchor='center')
            self.treeview3.column("电话", width=80, anchor='center')
            self.treeview3.column("密码", width=70, anchor='center')
            self.treeview3.heading("学号", text="学号")  # 显示表头
            self.treeview3.heading("姓名", text="姓名")
            self.treeview3.heading("性别", text="性别")
            self.treeview3.heading("生日", text="生日")
            self.treeview3.heading("电话", text="电话")
            self.treeview3.heading("密码", text="密码")

            self.treeview3.grid(row=1, column=0, rowspan=8, padx=10)
            # 插入查询结果
            self.cursor2.execute(search_sql1)
            self.row = self.cursor2.fetchone()  # 读取查询结果
            while self.row:
                self.treeview3.insert('', 0, values=(
                    self.row[0], self.row[1], self.row[2], self.row[3], self.row[4], self.row[5]))
                self.row = self.cursor2.fetchone()

            # 该生成绩显示表格框
            columns = ("学号", "课程号", "课程", "成绩")
            self.treeview4 = ttk.Treeview(root_smanage, height=18, show="headings", columns=columns)
            self.treeview4.column("学号", width=80, anchor='center')  # 表示列,不显示
            self.treeview4.column("课程号", width=70, anchor='center')
            self.treeview4.column("课程", width=100, anchor='center')
            self.treeview4.column("成绩", width=50, anchor='center')
            self.treeview4.heading("学号", text="学号")  # 显示表头
            self.treeview4.heading("课程号", text="课程号")
            self.treeview4.heading("课程", text="课程")
            self.treeview4.heading("成绩", text="成绩")

            self.treeview4.grid(row=1, column=1, rowspan=8, columnspan=3)

            # 框框
            self.frame_update = LabelFrame(root_smanage, text='修改信息', font=('微软雅黑', 16))
            self.frame_update.grid(row=0, column=6, padx=10, pady=10, rowspan=5)

            # 标签
            self.label_smanage1 = Label(root_smanage, text='学生表')
            self.label_smanage1.grid(row=0, column=0, padx=10, pady=10)
            self.label_smanage2 = Label(root_smanage, text='该生成绩表')
            self.label_smanage2.grid(row=0, column=2, padx=10, pady=10)
            self.label_score = Label(root_smanage, text='该科成绩:')
            self.label_score.grid(row=9, column=1, padx=10, pady=10)
            self.label_smanage_no = Label(self.frame_update, text='学号')
            self.label_smanage_no.grid(row=0, column=0, padx=10, pady=10)
            self.label_smanage_name = Label(self.frame_update, text='姓名')
            self.label_smanage_name.grid(row=1, column=0, padx=10, pady=10)
            self.label_smanage_sex = Label(self.frame_update, text='性别')
            self.label_smanage_sex.grid(row=2, column=0, padx=10, pady=10)
            self.label_smanage_birth = Label(self.frame_update, text='生日')
            self.label_smanage_birth.grid(row=3, column=0, padx=10, pady=10)
            self.label_smanage_tel = Label(self.frame_update, text='电话')
            self.label_smanage_tel.grid(row=4, column=0, padx=10, pady=10)
            self.label_smanage_pwd = Label(self.frame_update, text='密码')
            self.label_smanage_pwd.grid(row=5, column=0, padx=10, pady=10)

            # 按钮
            self.button_delete = Button(root_smanage, text='删除该学生', width=20, height=2, command=self.smanage_delete)
            self.button_delete.grid(row=9, column=0, padx=20, pady=20)
            self.button_score = Button(root_smanage, text='成绩更新', width=10, height=1, command=self.smanage_score)
            self.button_score.grid(row=9, column=3, padx=10, pady=10)
            self.button_smanage_insert = Button(root_smanage, text='插入学生', width=20, height=2,
                                                command=self.smanage_insert)
            self.button_smanage_insert.grid(row=5, column=6, padx=20, pady=20, rowspan=5)
            self.button_smanage_update = Button(self.frame_update, text="确定修改", width=10, height=1,
                                                command=self.smanage_update)
            self.button_smanage_update.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

            # 输入框
            self.varscore = StringVar
            self.var_smanage_no = StringVar
            self.var_smanage_name = StringVar
            self.var_smanage_sex = StringVar
            self.var_smanage_birth = StringVar
            self.var_smanage_tel = StringVar
            self.var_smanage_pwd = StringVar
            self.entry_score = Entry(root_smanage, textvariable=self.varscore)
            self.entry_score.grid(row=9, column=2, padx=15, pady=10)
            self.entry_smanage_no = Entry(self.frame_update, textvariable=self.var_smanage_no)
            self.entry_smanage_no.grid(row=0, column=1, padx=15, pady=10)
            self.entry_smanage_name = Entry(self.frame_update, textvariable=self.var_smanage_name)
            self.entry_smanage_name.grid(row=1, column=1, padx=15, pady=10)
            self.entry_smanage_sex = Entry(self.frame_update, textvariable=self.var_smanage_sex)
            self.entry_smanage_sex.grid(row=2, column=1, padx=15, pady=10)
            self.entry_smanage_birth = Entry(self.frame_update, textvariable=self.var_smanage_birth)
            self.entry_smanage_birth.grid(row=3, column=1, padx=15, pady=10)
            self.entry_smanage_tel = Entry(self.frame_update, textvariable=self.var_smanage_tel)
            self.entry_smanage_tel.grid(row=4, column=1, padx=15, pady=10)
            self.entry_smanage_pwd = Entry(self.frame_update, textvariable=self.var_smanage_no)
            self.entry_smanage_pwd.grid(row=5, column=1, padx=15, pady=10)

            # 单击---显示该生详细信息
            def treeview_click1(event):
                print('单击')
                item_text = []
                if self.treeview3.selection():
                    # 获取学生表展示信息值
                    for item in self.treeview3.selection():
                        item_text = self.treeview3.item(item, "values")
                        print(item_text[0])
                    # 绑定
                    self.temporary_sno = item_text[0]
                    self.temporary_sname = item_text[1]
                    self.temporary_sex = item_text[2]
                    self.temporary_birth = item_text[3]
                    self.temporary_tel = item_text[4]
                    self.temporary_pwd = item_text[5]
                    # 查询成绩
                    search_sql2 = "SELECT sc.tcid, c.cname, sc.score " \
                                  "FROM student_course sc " \
                                  "INNER JOIN course c ON sc.tcid = c.cno " \
                                  "WHERE sc.sno = %s"
                    self.cursor2.execute(search_sql2, (self.temporary_sno,))
                    self.row = self.cursor2.fetchone()  # 读取查询结果
                    del_button(self.treeview4)
                    while self.row:
                        self.treeview4.insert('', 0,
                                              values=(self.temporary_sno, self.row[0], self.row[1], self.row[2]))
                        self.row = self.cursor2.fetchone()

                    # 修改信息栏里显示信息
                    self.entry_smanage_no.delete(0, "end")
                    self.entry_smanage_no.insert(0, self.temporary_sno)
                    self.entry_smanage_name.delete(0, "end")
                    self.entry_smanage_name.insert(0, self.temporary_sname)
                    self.entry_smanage_sex.delete(0, "end")
                    self.entry_smanage_sex.insert(0, item_text[2])
                    self.entry_smanage_birth.delete(0, "end")
                    self.entry_smanage_birth.insert(0, item_text[3])
                    self.entry_smanage_tel.delete(0, "end")
                    self.entry_smanage_tel.insert(0, item_text[4])
                    self.entry_smanage_pwd.delete(0, "end")
                    self.entry_smanage_pwd.insert(0, item_text[5])
                    # 清空该科成绩框
                    self.entry_score.delete(0, "end")

            self.treeview3.bind('<ButtonRelease-1>', treeview_click1)  # 绑定单击离开事件

            # 单击---显示该科成绩
            def treeview_click2(event):
                print('单击')
                item_text = []
                if self.treeview4.selection():
                    for item in self.treeview4.selection():
                        item_text = self.treeview4.item(item, "values")
                        print(item_text[0])
                    self.temporary_cname = item_text[2]
                    self.temporary_cno = item_text[1]
                    self.entry_score.delete(0, "end")
                    self.entry_score.insert(0, item_text[3])

            self.treeview4.bind('<ButtonRelease-1>', treeview_click2)  # 绑定单击离开事件

            root_smanage.mainloop()

        def treeview_click(event):
            print('单击')
            item_text = []
            if self.treeview5.selection():
            # 获取课程表展示信息值
                for item in self.treeview5.selection():
                    item_text = self.treeview5.item(item, "values")
                    print(item_text[0])
            # 绑定
                self.temporary_cno = item_text[0]
            # 修改信息栏里显示信息
                self.entry_cno.delete(0, "end")
                self.entry_cno.insert(0, item_text[0])
                self.entry_cname.delete(0, "end")
                self.entry_cname.insert(0, item_text[1])
                self.entry_credit.delete(0, "end")
                self.entry_credit.insert(0, item_text[2])

            self.treeview5.bind('<ButtonRelease-1>', treeview_click)  # 绑定单击离开事件

    # 课程管理界面
    def cmanage(self):
        self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
        if self.connect:
            print('连接成功')
            print(self.no)  # 用户名, 即学号
            # 查询语句
            search_sql1 = "SELECT cno, cname, credit FROM course"
            # 创建游标
            self.cursor2 = self.connect.cursor()

            # 初始框的声明
            root_cmanage = Tk()
            root_cmanage.geometry("500x500+100+100")
            root_cmanage.title("课程管理系统")

            # 学生管理表格框
            columns = ("课程号", "名称", "学分")
            self.treeview5 = ttk.Treeview(root_cmanage, height=18, show="headings", columns=columns)
            self.treeview5.column("课程号", width=80, anchor='center')  # 表示列,不显示
            self.treeview5.column("名称", width=70, anchor='center')
            self.treeview5.column("学分", width=50, anchor='center')
            self.treeview5.heading("课程号", text="课程号")  # 显示表头
            self.treeview5.heading("名称", text="名称")
            self.treeview5.heading("学分", text="学分")

            self.treeview5.grid(row=1, column=0, rowspan=3, padx=10, pady=3)
            # 插入查询结果
            self.cursor2.execute(search_sql1)
            self.row = self.cursor2.fetchone()  # 读取查询结果
            while self.row:
                self.treeview5.insert('', 0, values=(self.row[0], self.row[1], self.row[2]))
                self.row = self.cursor2.fetchone()

            # 框框
            self.frame_cmanage = LabelFrame(root_cmanage, text='修改课程', font=('微软雅黑', 16))
            self.frame_cmanage.grid(row=1, column=1, padx=10, pady=10)

            # 标签
            self.label_cmanage1 = Label(root_cmanage, text='课程表')
            self.label_cmanage1.grid(row=0, column=0, padx=10, pady=10)
            self.label_cmanage_cno = Label(self.frame_cmanage, text='课程号:')
            self.label_cmanage_cno.grid(row=0, column=0, padx=10, pady=10)
            self.label_cmanage_cname = Label(self.frame_cmanage, text='课程名:')
            self.label_cmanage_cname.grid(row=1, column=0, padx=10, pady=10)
            self.label_cmanage_credit = Label(self.frame_cmanage, text='学分:')
            self.label_cmanage_credit.grid(row=2, column=0, padx=10, pady=10)

            # 按钮
            self.button_cmanage1 = Button(root_cmanage, text='选中课程删除', width=10, height=1, command=self.cmanage_delete)
            self.button_cmanage1.grid(row=4, column=0, padx=20, pady=20)
            self.button_cmanage_update = Button(self.frame_cmanage, text='确定修改', width=10, height=1,
                                                command=self.cmanage_update)
            self.button_cmanage_update.grid(row=4, column=0, padx=20, pady=20, columnspan=2)
            self.button_cmanage_insert = Button(root_cmanage, text='添加课程', width=20, height=2,
                                                command=self.cmanage_insert)
            self.button_cmanage_insert.grid(row=2, column=1, padx=10, pady=10)

            # 输入框
            self.var_cno = StringVar
            self.var_cname = StringVar
            self.var_credit = StringVar
            self.entry_cno = Entry(self.frame_cmanage, textvariable=self.var_cno)
            self.entry_cno.grid(row=0, column=1, padx=10, pady=10)
            self.entry_cname = Entry(self.frame_cmanage, textvariable=self.var_cname)
            self.entry_cname.grid(row=1, column=1, padx=10, pady=10)
            self.entry_credit = Entry(self.frame_cmanage, textvariable=self.var_credit)
            self.entry_credit.grid(row=2, column=1, padx=10, pady=10)

            def treeview_click1(event):
                print('单击')
                item_text = []
                if self.treeview5.selection():
                    # 获取课程表展示信息值
                    for item in self.treeview5.selection():
                        item_text = self.treeview5.item(item, "values")
                        print(item_text[0])
                    self.temporary_cno = item_text[0]
                    # 修改信息栏里显示信息
                    self.entry_cno.delete(0, "end")
                    self.entry_cno.insert(0, item_text[0])
                    self.entry_cname.delete(0, "end")
                    self.entry_cname.insert(0, item_text[1])
                    self.entry_credit.delete(0, "end")
                    self.entry_credit.insert(0, item_text[2])

            self.treeview5.bind('<ButtonRelease-1>', treeview_click1)  # 绑定单击离开事件

            root_cmanage.mainloop()

    # ======== smanage中"删除该生"按钮
    def smanage_delete(self):
        if self.temporary_sno != '':
            # 链接数据库
            self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
            try:
                if self.connect:
                    print('连接成功')
                    print(self.no)  # 用户名, 即学号

                    # 开始事务
                    self.connect.begin()

                    # 查询语句
                    delete_student_sql = "DELETE FROM student WHERE sno=%s"
                    delete_student_pwd_sql = "DELETE FROM student_pwd WHERE user=%s"

                    # 创建游标
                    self.cursor2 = self.connect.cursor()

                    # 执行删除操作
                    self.cursor2.execute(delete_student_sql, (self.temporary_sno,))
                    self.cursor2.execute(delete_student_pwd_sql, (self.temporary_sno,))

                    # 提交事务
                    self.connect.commit()
                    messagebox.showinfo(title='提示', message='删除成功!')

                    # 重置treeview3
                    del_button(self.treeview3)
                    search_sql = """
                    SELECT sno, sname, sex, birthday, tel, pwd 
                    FROM student 
                    INNER JOIN student_pwd ON student.sno = student_pwd.user
                    """
                    self.cursor2.execute(search_sql)
                    self.row = self.cursor2.fetchone()  # 读取查询结果
                    while self.row:
                        self.treeview3.insert('', 0, values=(
                            self.row[0], self.row[1], self.row[2], self.row[3], self.row[4], self.row[5]))
                        self.row = self.cursor2.fetchone()

            except pymysql.Error as e:
                # 出现异常时回滚
                self.connect.rollback()
                messagebox.showinfo(title='数据库错误', message=str(e))
            finally:
                self.cursor2.close()
                self.connect.close()
        else:
            messagebox.showinfo(title='提示', message='未选中, 请选中学生')

    # ======== smanage中"更新成绩"按钮
    def del_button(tree):
        x = tree.get_children()
        for item in x:
            tree.delete(item)

    def refresh_student_course(self):
        del_button(self.treeview4)
        search_sql2 = "SELECT sc.tcid, c.cname, sc.score " \
                      "FROM student_course sc " \
                      "INNER JOIN course c ON sc.tcid = c.cno " \
                      "WHERE sc.sno = %s"
        self.cursor2.execute(search_sql2, (self.temporary_sno,))
        self.row = self.cursor2.fetchone()  # 读取查询结果
        while self.row:
            self.treeview4.insert('', 0,
                                  values=(self.temporary_sno, self.row[0], self.row[1], self.row[2]))
            self.row = self.cursor2.fetchone()

    def smanage_score(self):
        if self.entry_score.get() != '':
            # 连接数据库
            self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
            self.cursor2 = self.connect.cursor()  # 创建游标

            if self.connect:
                print('连接成功')
                print(self.no)
                sql_student_score = "UPDATE student_course SET score=%s WHERE sno=%s AND tcid=%s"
                self.cursor2.execute(sql_student_score,
                                     (self.entry_score.get(), self.temporary_sno, self.temporary_cno))
                self.connect.commit()
                messagebox.showinfo(title='提示', message='成绩更新成功!')

                # 重置treeview4
                self.refresh_student_course()

        else:
            messagebox.showinfo(title='提示', message='请勿更新空成绩!')

    # ========= smanage中的"修改信息"按钮
    def smanage_update(self):
        if self.entry_smanage_no.get() == self.temporary_sno:
            self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
            self.cursor2 = self.connect.cursor()  # 创建游标
            sql_up = "UPDATE student SET sname=%s, sex=%s, birthday=%s, tel=%s WHERE sno=%s"
            if self.connect:
                print('连接成功')
                print(self.no)
                self.cursor2.execute(sql_up, (self.entry_smanage_name.get(),
                                              self.entry_smanage_sex.get(),
                                              self.entry_smanage_birth.get(),
                                              self.entry_smanage_tel.get(),
                                              self.temporary_sno))
                self.connect.commit()
                sql_up2 = "UPDATE student_pwd SET pwd=%s WHERE user=%s"
                self.cursor2.execute(sql_up2, (self.entry_smanage_pwd.get(), self.temporary_sno))
                self.connect.commit()
                messagebox.showinfo(title='提示', message='课程信息修改成功!')

                # 修改treeview3中值
                sql_up3 = "SELECT sno, sname, sex, birthday, tel, pwd " \
                          "FROM student " \
                          "INNER JOIN student_pwd ON sno = user"
                del_button(self.treeview3)
                self.cursor2.execute(sql_up3)
                self.row = self.cursor2.fetchone()
                while self.row:
                    self.treeview3.insert('', 0,
                                          values=(self.row[0],
                                                  self.row[1],
                                                  self.row[2],
                                                  self.row[3],
                                                  self.row[4],
                                                  self.row[5]))
                    self.row = self.cursor2.fetchone()
        else:
            messagebox.showinfo(title='提示', message='请勿修改学号!')

    # ========= smanage中的插入学生界面
    def smanage_insert(self):
        root.window = Tk()  # 初始框的声明
        root.window.geometry('300x250+100+100')
        root.window.title('添加学生')
        # 框框
        self.frame_smanage_insert = LabelFrame(root.window)
        self.frame_smanage_insert.grid(padx=30, pady=30)
        # Label
        self.label_smanage_insert_sno = Label(self.frame_smanage_insert, text='学号：')
        self.label_smanage_insert_sno.grid(row=0, column=0, padx=10, pady=10)
        self.label_smanage_insert_sname = Label(self.frame_smanage_insert, text='姓名：')
        self.label_smanage_insert_sname.grid(row=1, column=0, padx=10, pady=10)
        self.label_smanage_insert_pwd = Label(self.frame_smanage_insert, text='初始密码为学号!')
        self.label_smanage_insert_pwd.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        # 输入框
        self.var_smanage_insert_sno = StringVar
        self.var_smanage_insert_sname = StringVar
        self.entry_smanage_insert_sno = Entry(self.frame_smanage_insert, textvariable=self.var_smanage_insert_sno)
        self.entry_smanage_insert_sno.grid(row=0, column=1, padx=10, pady=10)
        self.entry_smanage_insert_sname = Entry(self.frame_smanage_insert, textvariable=self.var_smanage_insert_sname)
        self.entry_smanage_insert_sname.grid(row=1, column=1, padx=10, pady=10)
        # 按钮
        self.button_ok = Button(self.frame_smanage_insert, text='确定', command=self.smanage_insert_ok)
        self.button_ok.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # ========= smanage_insert中的"插入学生"按钮
    def smanage_insert_ok(self):
        # 连接数据库
        self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
        self.cursor2 = self.connect.cursor()
        sno = self.entry_smanage_insert_sno.get()
        sname = self.entry_smanage_insert_sname.get()

        # 使用参数化查询安全插入学生信息
        sql_insert1 = "INSERT INTO student (sno, sname) VALUES (%s, %s)"
        try:
            self.cursor2.execute(sql_insert1, (sno, sname))
            self.connect.commit()

            # 插入学生密码信息，初始密码设置为学号
            sql_insert2 = "INSERT INTO student_pwd (user, pwd) VALUES (%s, %s)"
            self.cursor2.execute(sql_insert2, (sno, sno))
            self.connect.commit()

            messagebox.showinfo(title='提示', message='插入成功!')

            # 重新创建游标
            self.cursor2.close()
            self.cursor2 = self.connect.cursor()

            # 修改treeview3中信息
            sql_insert3 = "SELECT sno, sname, sex, birthday, tel, pwd " \
                          "FROM student " \
                          "INNER JOIN student_pwd " \
                          "WHERE sno=user"
            del_button(self.treeview3)
            self.cursor2.execute(sql_insert3)
            self.row = self.cursor2.fetchone()
            while self.row:
                self.treeview3.insert('', 0,
                                      values=(self.row[0],
                                              self.row[1],
                                              self.row[2],
                                              self.row[3],
                                              self.row[4],
                                              self.row[5]))
                self.row = self.cursor2.fetchone()

        except pymysql.Error as e:
            # 检查错误消息是否包含触发器的错误消息
            if '学号长度必须为7位' in str(e):
                messagebox.showinfo(title='长度错误', message='学号长度必须为7位，请重试!')
            else:
                messagebox.showinfo(title='数据库错误', message=str(e))
        finally:
            self.cursor2.close()
            self.connect.close()

    def cmanage_delete(self):
        # 检查是否选中课程
        if self.temporary_cno != '':
            # 链接数据库
            self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
            try:
                if self.connect:
                    print('连接成功')
                    print(self.no)  # 用户名, 即工号

                    # 开始事务
                    self.connect.begin()

                    # 删除语句
                    delete_course_sql = "DELETE FROM course WHERE cno=%s"
                    delete_student_course_sql = "DELETE FROM student_course WHERE tcid=%s"

                    # 创建游标
                    self.cursor2 = self.connect.cursor()

                    # 输出调试信息，检查临时课程号是否正确
                    print(f"Deleting course with cno={self.temporary_cno}")

                    # 执行删除操作
                    self.cursor2.execute(delete_course_sql, (self.temporary_cno,))
                    self.cursor2.execute(delete_student_course_sql, (self.temporary_cno,))

                    # 提交事务
                    self.connect.commit()
                    messagebox.showinfo(title='提示', message='删除成功!')

                    # 重置课程列表视图
                    self.refresh_course_list()

            except pymysql.Error as e:
                # 出现异常时回滚
                self.connect.rollback()
                messagebox.showinfo(title='数据库错误', message=str(e))
            finally:
                self.cursor2.close()
                self.connect.close()
        else:
            messagebox.showinfo(title='提示', message='未选中课程，请选中课程')

    def refresh_course_list(self):
        # 重置treeview5
        del_button(self.treeview5)
        search_sql1 = "SELECT cno, cname, credit FROM course"
        self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
        self.cursor2 = self.connect.cursor()
        self.cursor2.execute(search_sql1)
        self.row = self.cursor2.fetchone()  # 读取查询结果
        while self.row:
            self.treeview5.insert('', 0, values=(self.row[0], self.row[1], self.row[2]))
            self.row = self.cursor2.fetchone()
        self.cursor2.close()
        self.connect.close()

    # 清空treeview
    def del_button(tree):
        x = tree.get_children()
        for item in x:
            tree.delete(item)

    # ========= cmanage中插入课程界面
    def cmanage_insert(self):
        root.window = Tk()  # 初始框的声明
        root.window.geometry('300x250+100+100')
        root.window.title('添加课程')
        # 框框
        self.frame_cmanage_insert = LabelFrame(root.window)
        self.frame_cmanage_insert.grid(padx=30, pady=30)
        # Label
        self.label_cmanage_insert_cno = Label(self.frame_cmanage_insert, text='课程号：')
        self.label_cmanage_insert_cno.grid(row=0, column=0, padx=10, pady=10)
        self.label_cmanage_insert_cname = Label(self.frame_cmanage_insert, text='课程名：')
        self.label_cmanage_insert_cname.grid(row=1, column=0, padx=10, pady=10)
        self.label_cmanage_insert_credit = Label(self.frame_cmanage_insert, text='学分:')
        self.label_cmanage_insert_credit.grid(row=2, column=0, padx=10, pady=10)
        # 输入框
        self.var_cmanage_insert_cno = StringVar
        self.var_cmanage_insert_cname = StringVar
        self.var_cmanage_insert_credit = StringVar
        self.entry_cmanage_insert_cno = Entry(self.frame_cmanage_insert, textvariable=self.var_cmanage_insert_cno)
        self.entry_cmanage_insert_cno.grid(row=0, column=1, padx=10, pady=10)
        self.entry_cmanage_insert_cname = Entry(self.frame_cmanage_insert, textvariable=self.var_cmanage_insert_cname)
        self.entry_cmanage_insert_cname.grid(row=1, column=1, padx=10, pady=10)
        self.entry_cmanage_insert_credit = Entry(self.frame_cmanage_insert, textvariable=self.var_cmanage_insert_credit)
        self.entry_cmanage_insert_credit.grid(row=2, column=1, padx=10, pady=10)
        # 按钮
        self.button_ok = Button(self.frame_cmanage_insert, text='确定', command=self.cmanage_insert_ok)
        self.button_ok.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # ========= cmanage中"更新"按钮
    # ========= cmanage中"更新"按钮
    def cmanage_update(self):
        if self.entry_cno.get() == self.temporary_cno:
            self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
            self.cursor2 = self.connect.cursor()  # 创建游标
            sql_call_proc = "CALL update_course_and_student_course(%s, %s)"

            try:
                if self.connect:
                    print('连接成功')
                    print(self.no)

                    # 开始事务
                    self.connect.begin()

                    # 调用存储过程更新课程信息和学生课程信息
                    self.cursor2.execute(sql_call_proc, (self.temporary_cno, self.entry_cname.get()))

                    # 提交事务
                    self.connect.commit()
                    messagebox.showinfo(title='提示', message='信息修改成功!')

                    # 修改treeview5中值
                    sql_up3 = "SELECT cno, cname, credit FROM course"
                    del_button(self.treeview5)
                    # 插入查询结果
                    self.cursor2.execute(sql_up3)
                    self.row = self.cursor2.fetchone()  # 读取查询结果
                    while self.row:
                        self.treeview5.insert('', 0, values=(self.row[0], self.row[1], self.row[2]))
                        self.row = self.cursor2.fetchone()

            except pymysql.Error as e:
                # 出现异常时回滚
                self.connect.rollback()
                messagebox.showinfo(title='数据库错误', message=str(e))
            finally:
                self.cursor2.close()
                self.connect.close()
        else:
            messagebox.showinfo(title='提示', message='请勿修改课程号!')

    def cmanage_insert_ok(self):
        # 连接数据库
        self.connect = pymysql.connect(host=self.ip, port=self.port, user=self.id, passwd=self.pd, db=self.db)
        self.cursor2 = self.connect.cursor()  # 创建游标
        cno = self.entry_cmanage_insert_cno.get()
        cname = self.entry_cmanage_insert_cname.get()
        credit = self.entry_cmanage_insert_credit.get()
        sql_insert1 = "INSERT INTO course (cno, cname, credit) VALUES (%s, %s, %s)"
        try:
            self.cursor2.execute(sql_insert1, (cno, cname, credit))
            self.connect.commit()
            messagebox.showinfo(title='提示', message='插入成功!')
        except pymysql.Error as e:
            messagebox.showinfo(title='数据库错误', message=str(e))

            # 修改treeview5中值
            sql_up3 = "SELECT cno, cname, credit FROM course"
            del_button(self.treeview5)
            # 插入查询结果
            self.cursor2.execute(sql_up3)
            self.row = self.cursor2.fetchone()  # 读取查询结果
            while self.row:
                self.treeview5.insert('', 0, values=(self.row[0], self.row[1], self.row[2]))
                self.row = self.cursor2.fetchone()


# 清空treeview
def del_button(tree):
    x = tree.get_children()
    for item in x:
        tree.delete(item)


if __name__ == '__main__':
    # 初始化Tk()
    root = Tk()
    Basedesk(root)
    # 进入消息循环 mainloop()
    mainloop()
