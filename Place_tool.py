# coding:gbk
# *******************************************
# ����: �Җ|
# mail:wodong526@dingtalk.com
# time:2022/3/1
# �汾��V1.5
# ******************************************
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from pymel.core.datatypes import Matrix, Vector, TransformationMatrix
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.cmds as mc
import pymel.core as pm
import random
import math

edition = 'V1.5'  # �汾��


def maya_main_window():
    main_window_par = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_par), QtWidgets.QWidget)


class PlaceObj(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(PlaceObj, self).__init__(parent)

        self.setWindowTitle(u'�|����������.{}'.format(edition))
        self.setMinimumWidth(300)
        self.setMinimumHeight(400)

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)  # ȥ�������ϵ��ʺ�

        self.crea_widgets()
        self.crea_layouts()
        self.crea_connections()

    def crea_widgets(self):
        self.floor_lin = QtWidgets.QLineEdit()
        self.floor_lin.setPlaceholderText(u'����������')
        self.floor_lin.setMinimumHeight(30)
        self.floor_lin.setFont(QtGui.QFont('����', 10))
        self.tree_lin = QtWidgets.QLineEdit()
        self.tree_lin.setPlaceholderText(u'������ö���')
        self.tree_lin.setMinimumHeight(30)
        self.tree_lin.setFont(QtGui.QFont('����', 10))

        self.spacer = QtWidgets.QSpacerItem(10, 15, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)  # ����

        self.line_v = QtWidgets.QFrame()  # �ָ���
        self.line_v.setFrameShape(QtWidgets.QFrame.VLine)
        # self.line_v.setLineWidth(5)
        # self.line_v.setMidLineWidth(10)
        self.line_v.setFrameShadow(QtWidgets.QFrame.Raised)

        self.line_h_up = QtWidgets.QFrame()
        self.line_h_up.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_h_up.setFrameShadow(QtWidgets.QFrame.Raised)

        self.line_h_mid = QtWidgets.QFrame()
        self.line_h_mid.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_h_mid.setFrameShadow(QtWidgets.QFrame.Raised)

        self.line_h_down = QtWidgets.QFrame()
        self.line_h_down.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_h_down.setFrameShadow(QtWidgets.QFrame.Raised)

        cbox_lis = [u'soft', u'undulate', u'rot', u'scl', u'normals', u'localOrWord']
        self.cbox_dir = {}
        for inf in cbox_lis:
            cbox = QtWidgets.QCheckBox()
            cbox.setCursor(QtCore.Qt.PointingHandCursor)
            self.cbox_dir[inf + '_cbox'] = cbox
        self.cbox_dir[u'normals_cbox'].setText(u' ')
        self.cbox_dir[u'localOrWord_cbox'].setText(u'��ǰΪ������ת')

        self.soft_vle_sbox = QtWidgets.QSpinBox()
        self.soft_vle_sbox.setMinimumHeight(15)
        self.soft_vle_sbox.setMinimum(1)
        self.soft_vle_sbox.setMaximum(9999)
        if mc.softSelect(sse=1, q=True) == True:
            self.cbox_dir[u'soft_cbox'].setChecked(True)
            self.soft_vle_sbox.setReadOnly(False)
        else:
            self.cbox_dir[u'soft_cbox'].setChecked(False)
            self.soft_vle_sbox.setReadOnly(True)

        dsbox_lis = [u'undulate_vle', u'rot_min', u'rot_max', u'scl_min', u'scl_max']
        dsbox_prefix = [u'', u'��', u'��', u'', u'']
        dsbox_suffix = [u' cm', u'  ��', u'  ��', u'  /1', u'  /1']
        dsbox_min = [-999, 0, 0, -999, -999]
        dsbox_max = [9999, 360, 360, 9999, 9999]
        self.dsbox_dir = {}
        for inf in range(len(dsbox_lis)):
            dsbox = QtWidgets.QDoubleSpinBox()
            dsbox.setReadOnly(True)
            dsbox.setMinimumHeight(15)
            dsbox.setDecimals(3)
            dsbox.setSingleStep(0.1)
            dsbox.setMinimum(dsbox_min[inf])
            dsbox.setMaximum(dsbox_max[inf])
            dsbox.setPrefix(dsbox_prefix[inf])
            dsbox.setSuffix(dsbox_suffix[inf])
            self.dsbox_dir[dsbox_lis[inf] + '_dsbox'] = dsbox

        str_lis = [u'��ѡ��', u'����', u'ֵ', u'��Χ', u'����', u'��ת', u'����', u'mini', u'max', u'���ڵ��淨��']
        num_lis = [1, 1, 1, 2, 1, 1, 1, 2, 2, 1]
        self.lab_dir = {}
        for inf in zip(str_lis, num_lis):
            for num in range(inf[1]):
                label = QtWidgets.QLabel()
                label.setText(u'{}'.format(inf[0]))
                label.setFont(QtGui.QFont('����', 15))
                self.lab_dir[inf[0] + '_' + str(num)] = label

        but_lis = [u'����', u'  ��', u'�� R U N ��']
        but_size = [15, 15, 30]
        self.but_dir = {}
        for inf in zip(but_lis, but_size):
            button = QtWidgets.QPushButton()
            button.setText(inf[0])
            button.setFont(QtGui.QFont('����', inf[1]))
            self.but_dir[inf[0]] = button
        self.but_dir[u'�� R U N ��'].setMinimumHeight(50)

    def crea_layouts(self):
        floor_layout = QtWidgets.QHBoxLayout()
        floor_layout.addWidget(self.but_dir[u'����'])
        floor_layout.addWidget(self.floor_lin)

        tree_layout = QtWidgets.QHBoxLayout()
        tree_layout.addWidget(self.but_dir[u'  ��'])
        tree_layout.addWidget(self.tree_lin)

        sofOrUnd_layout = QtWidgets.QHBoxLayout()
        sofOrUnd_layout.addWidget(self.lab_dir[u'��ѡ��_0'])
        sofOrUnd_layout.addWidget(self.cbox_dir[u'soft_cbox'])
        sofOrUnd_layout.addWidget(self.lab_dir[u'����_0'])
        sofOrUnd_layout.addWidget(self.soft_vle_sbox)
        sofOrUnd_layout.addWidget(self.line_v)
        sofOrUnd_layout.addWidget(self.lab_dir[u'����_0'])
        sofOrUnd_layout.addWidget(self.cbox_dir[u'undulate_cbox'])
        sofOrUnd_layout.addWidget(self.lab_dir[u'ֵ_0'])
        sofOrUnd_layout.addWidget(self.dsbox_dir[u'undulate_vle_dsbox'])

        rot_layout = QtWidgets.QHBoxLayout()
        rot_layout.addWidget(self.lab_dir[u'��ת_0'])
        rot_layout.addWidget(self.cbox_dir[u'rot_cbox'])
        rot_layout.addWidget(self.lab_dir[u'mini_0'])
        rot_layout.addWidget(self.dsbox_dir[u'rot_min_dsbox'])
        rot_layout.addWidget(self.lab_dir[u'max_0'])
        rot_layout.addWidget(self.dsbox_dir[u'rot_max_dsbox'])

        scl_layout = QtWidgets.QHBoxLayout()
        scl_layout.addWidget(self.lab_dir[u'����_0'])
        scl_layout.addWidget(self.cbox_dir[u'scl_cbox'])
        scl_layout.addWidget(self.lab_dir[u'mini_1'])
        scl_layout.addWidget(self.dsbox_dir[u'scl_min_dsbox'])
        scl_layout.addWidget(self.lab_dir[u'max_1'])
        scl_layout.addWidget(self.dsbox_dir[u'scl_max_dsbox'])

        nor_layout = QtWidgets.QHBoxLayout()
        nor_layout.addWidget(self.lab_dir[u'���ڵ��淨��_0'])
        nor_layout.addWidget(self.cbox_dir[u'normals_cbox'])
        nor_layout.addWidget(self.cbox_dir[u'localOrWord_cbox'])
        nor_layout.setSpacing(5)
        nor_layout.addItem(self.spacer)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(floor_layout)
        main_layout.addLayout(tree_layout)
        main_layout.addWidget(self.line_h_up)
        main_layout.addLayout(sofOrUnd_layout)
        main_layout.addWidget(self.line_h_mid)
        main_layout.addLayout(rot_layout)
        main_layout.addLayout(scl_layout)
        main_layout.addWidget(self.line_h_down)
        main_layout.addLayout(nor_layout)
        main_layout.addWidget(self.but_dir[u'�� R U N ��'])

    def crea_connections(self):
        self.but_dir[u'����'].clicked.connect(self.select_floor_obj)
        self.but_dir[u'  ��'].clicked.connect(self.select_tree_obj)

        self.cbox_dir[u'soft_cbox'].stateChanged.connect(self.sof_vle_TorF)
        self.cbox_dir[u'undulate_cbox'].stateChanged.connect(self.sof_vle_TorF)
        self.cbox_dir[u'rot_cbox'].stateChanged.connect(self.sof_vle_TorF)
        self.cbox_dir[u'scl_cbox'].stateChanged.connect(self.sof_vle_TorF)
        self.cbox_dir[u'localOrWord_cbox'].stateChanged.connect(self.sof_vle_TorF)

        self.but_dir[u'�� R U N ��'].clicked.connect(self.crea_run)

    def crea_run(self):
        floor_lis = self.floor_lin.text()
        tree_lis = self.tree_lin.text()
        print floor_lis, tree_lis

        world_objs = mc.ls(type='transform')
        if floor_lis == '' or tree_lis == '':
            print '����������ͷ������岻��Ϊ�ա�'
            return False
        else:
            floor_obj = floor_lis.split(',')
            for inf in floor_obj:
                if inf not in world_objs:
                    print '����{}�����ڡ�'.format(inf)
                    return False

            tree_obj = tree_lis.split(',')
            for inf in tree_obj:
                if inf not in world_objs:
                    print '����{}�����ڡ�'.format(inf)
                    return False

        if mc.softSelect(sse=True, q=True) == True:
            self.cbox_dir[u'soft_cbox'].setChecked(True)
        elif mc.softSelect(sse=True, q=True) == False:
            self.cbox_dir[u'soft_cbox'].setChecked(False)

        sToe = 'screenToEnvironment'
        if mc.draggerContext('screenToEnvironment', ex=True, q=True):
            mc.deleteUI('screenToEnvironment')
        mc.draggerContext('screenToEnvironment', pc=self.selSpot_2d_click, dc=self.selSpot_2d_drag, n=sToe,
                          cur='crossHair')
        mc.setToolTo('screenToEnvironment')

    def run_cultivate(self, pos_point, dire_vector):
        floor_obj = self.floor_lin.text().split(',')
        tree_obj = self.tree_lin.text().split(',')

        for trans_obj in floor_obj:
            mesh_obj = mc.listRelatives(trans_obj, shapes=True)[0]
            sel_lis = om.MSelectionList()
            sel_lis.add(mesh_obj)

            sel_dag_node = om.MDagPath()
            sel_lis.getDagPath(0, sel_dag_node)
            fn_mesh = om.MFnMesh(sel_dag_node)

            hitPoint = om.MFloatPoint()

            hitDistance = om.MScriptUtil(0.0)
            hitRayParam = hitDistance.asFloatPtr()

            hitFace = om.MScriptUtil()
            hitFacePtr = hitFace.asIntPtr()
            hitTriangle = om.MScriptUtil()
            hitTrianglePtr = hitTriangle.asIntPtr()

            fn_mesh.closestIntersection(om.MFloatPoint(pos_point),
                                        om.MFloatVector(dire_vector),
                                        None,
                                        None,
                                        False,
                                        om.MSpace.kWorld,
                                        99999,
                                        True,
                                        None,
                                        hitPoint,  # ���е����������
                                        hitRayParam,  # ���е�����Ļ�����߾���
                                        hitFacePtr,  # ���е�����id
                                        hitTrianglePtr,  # ���е�����������id
                                        None,
                                        None)

            tree_x, tree_y, tree_z, _ = hitPoint
            if (tree_x, tree_y, tree_z) != (0.0, 0.0, 0.0):
                tree_dup_num = random.randint(0, (len(tree_obj) - 1))

                dup_obj = mc.duplicate(tree_obj[tree_dup_num], rr=1)[0]
                mc.setAttr('{}.translate'.format(dup_obj), tree_x, tree_y, tree_z)

                if self.cbox_dir[u'normals_cbox'].isChecked() == True:
                    self.outPrint(hitFacePtr, dup_obj, trans_obj, fn_mesh)

                if self.cbox_dir[u'undulate_cbox'].isChecked() == True:
                    self.crea_undulate(dup_obj)

                if self.cbox_dir[u'rot_cbox'].isChecked() == True:
                    self.crea_rotate(dup_obj)

                if self.cbox_dir[u'scl_cbox'].isChecked() == True:
                    self.crea_scale(dup_obj)

                mc.select(dup_obj)

            else:
                continue

            # mc.waitCursor(state = True)

    def crea_undulate(self, dup_obj):
        mc.move(float(self.dsbox_dir[u'undulate_vle_dsbox'].cleanText()), dup_obj, y=True, r=1)

    def crea_rotate(self, dup_obj):
        rot_vle = random.uniform(float(self.dsbox_dir[u'rot_min_dsbox'].cleanText()),
                                 float(self.dsbox_dir[u'rot_max_dsbox'].cleanText()))
        mc.rotate(rot_vle, dup_obj, y=True, r=True)

    def crea_scale(self, dup_obj):
        scl_vle = random.uniform(float(self.dsbox_dir[u'scl_min_dsbox'].cleanText()),
                                 float(self.dsbox_dir[u'scl_max_dsbox'].cleanText()))
        mc.scale(scl_vle, scl_vle, scl_vle, dup_obj, r=True)

    def selSpot_2d_click(self):
        X_spot, Y_spot, _ = mc.draggerContext('screenToEnvironment', query=True, ap=True)
        position_point = om.MPoint()
        direction_vector = om.MVector()

        if mc.softSelect(sse=True, q=True) == True:
            self.cbox_dir[u'soft_cbox'].setChecked(True)
            soft_radiu = mc.softSelect(ssd=True, q=True) * 2

            for inf in range(self.soft_vle_sbox.value()):
                pos_x_vle = random.uniform((X_spot - soft_radiu), (X_spot + soft_radiu))
                pos_y_vle = random.uniform((Y_spot - soft_radiu), (Y_spot + soft_radiu))

                world_viw = omui.M3dView.active3dView()
                world_viw.viewToWorld(int(pos_x_vle), int(pos_y_vle), position_point, direction_vector)
                self.run_cultivate(position_point, direction_vector)
        else:
            self.cbox_dir[u'soft_cbox'].setChecked(False)
            world_viw = omui.M3dView.active3dView()
            world_viw.viewToWorld(int(X_spot), int(Y_spot), position_point, direction_vector)
            self.run_cultivate(position_point, direction_vector)

    def selSpot_2d_drag(self):
        X_spot, Y_spot, _ = mc.draggerContext('screenToEnvironment', query=True, dp=True)
        position_point = om.MPoint()
        direction_vector = om.MVector()

        if mc.softSelect(sse=True, q=True) == True:
            self.cbox_dir[u'soft_cbox'].setChecked(True)
            soft_radiu = mc.softSelect(ssd=True, q=True) * 2

            for inf in range(self.soft_vle_sbox.value()):
                pos_x_vle = random.uniform((X_spot - soft_radiu), (X_spot + soft_radiu))
                pos_y_vle = random.uniform((Y_spot - soft_radiu), (Y_spot + soft_radiu))

                world_viw = omui.M3dView.active3dView()
                world_viw.viewToWorld(int(pos_x_vle), int(pos_y_vle), position_point, direction_vector)
                self.run_cultivate(position_point, direction_vector)
        else:
            self.cbox_dir[u'soft_cbox'].setChecked(False)
            world_viw = omui.M3dView.active3dView()
            world_viw.viewToWorld(int(X_spot), int(Y_spot), position_point, direction_vector)
            self.run_cultivate(position_point, direction_vector)

    def select_floor_obj(self):
        self.floor_lin.setText(','.join(mc.ls(sl=True)))

    def select_tree_obj(self):
        self.tree_lin.setText(','.join(mc.ls(sl=True)))

    def outPrint(self, num, dup_obj, trans_obj, mesh):
        face_num = om.MScriptUtil().getInt(num)
        normals = om.MFloatVectorArray()

        mc.select(cl=True)

        mc.select('{}.f[{}]'.format(trans_obj, face_num))
        mc.select(mc.polyListComponentConversion(tv=True))
        face_vtxLis = []
        for inf in mc.ls(sl=True):
            if ':' not in inf:
                face_vtxLis.append(int(inf[inf.index('[') + 1]))
            elif ':' in inf:
                vtx_id_lis = self.extract(inf).split(':')
                [face_vtxLis.append(vtx_id) for vtx_id in range(int(vtx_id_lis[0]), (int(vtx_id_lis[1]) + 1))]

        if len(face_vtxLis) <= 2:
            print '���е���ֻ��������ӵ㣬�޷��ж����߷���'
            return False

        points = [Vector(pm.xform('{}.vtx[{}]'.format(trans_obj, i), q=True, t=True, ws=True)) for i in
                  range(int(face_vtxLis[0]), (int(face_vtxLis[2])) + 1)]
        local_x = (points[1] - points[0]).normal()
        local_z = (points[2] - points[0]).normal()
        #        local_y = local_x.cross(local_z).normal() ��������ֱ��������������ڸ�������mesh�ϻ������⣬��������һ����������淨����������y��
        local_y = self.getY_vector(num, mesh)

        centroid = sum(points) / 4.0
        face_matrix = TransformationMatrix(local_x.x, local_x.y, local_x.z, 0,
                                           local_y.x, local_y.y, local_y.z, 0,
                                           local_z.x, local_z.y, local_z.z, 0,
                                           centroid.x, centroid.y, centroid.z, 1)

        obj_rot = face_matrix.getRotation() * (180 / math.pi)

        if self.cbox_dir[u'localOrWord_cbox'].isChecked() == False:
            mc.setAttr('{}.rotate'.format(dup_obj), obj_rot[0], obj_rot[1], obj_rot[2])
        elif self.cbox_dir[u'localOrWord_cbox'].isChecked() == True:
            old_rot = mc.getAttr('{}.rotate'.format(dup_obj))[0]
            print old_rot
            mc.setAttr('{}.rotate'.format(dup_obj), (obj_rot[0] + old_rot[0]),
                       (obj_rot[1] + old_rot[1]),
                       (obj_rot[2] + old_rot[2]))
        mc.select(cl=True)

    def getY_vector(self, num, fn_mesh):
        face_num = om.MScriptUtil().getInt(num)
        normals = om.MFloatVectorArray()
        fn_mesh.getFaceVertexNormals(face_num, normals, om.MSpace.kWorld)

        face_pointLis = []
        face_poinNum = normals.length()
        for inf in range(face_poinNum):
            face_pointLis.append([normals[inf].x, normals[inf].y, normals[inf].z])

        face_normal_x = int()
        face_normal_y = int()
        face_normal_z = int()
        for inf in range(len(face_pointLis)):
            face_normal_x = face_normal_x + face_pointLis[inf][0]
            face_normal_y = face_normal_y + face_pointLis[inf][1]
            face_normal_z = face_normal_z + face_pointLis[inf][2]

        face_normal = [face_normal_x / face_poinNum, face_normal_y / face_poinNum, face_normal_z / face_poinNum]
        return Vector(face_normal)

    def extract(self, string, start='[', stop=']'):
        return string[string.index(start) + 1: string.index(stop)]

    def sof_vle_TorF(self, bol):
        # ���и�ѡ�����
        if self.cbox_dir[u'soft_cbox'].isChecked() == True:
            mc.softSelect(sse=True, e=True)
            self.soft_vle_sbox.setReadOnly(False)
        if self.cbox_dir[u'soft_cbox'].isChecked() == False:
            mc.softSelect(sse=False, e=True)
            self.soft_vle_sbox.setReadOnly(True)
        if self.cbox_dir[u'undulate_cbox'].isChecked() == True:
            self.dsbox_dir[u'undulate_vle_dsbox'].setReadOnly(False)
        if self.cbox_dir[u'undulate_cbox'].isChecked() == False:
            self.dsbox_dir[u'undulate_vle_dsbox'].setReadOnly(True)
        if self.cbox_dir[u'rot_cbox'].isChecked() == True:
            self.dsbox_dir[u'rot_min_dsbox'].setReadOnly(False)
            self.dsbox_dir[u'rot_max_dsbox'].setReadOnly(False)
        if self.cbox_dir[u'rot_cbox'].isChecked() == False:
            self.dsbox_dir[u'rot_min_dsbox'].setReadOnly(True)
            self.dsbox_dir[u'rot_max_dsbox'].setReadOnly(True)
        if self.cbox_dir[u'scl_cbox'].isChecked() == True:
            self.dsbox_dir[u'scl_min_dsbox'].setReadOnly(False)
            self.dsbox_dir[u'scl_max_dsbox'].setReadOnly(False)
        if self.cbox_dir[u'scl_cbox'].isChecked() == False:
            self.dsbox_dir[u'scl_min_dsbox'].setReadOnly(True)
            self.dsbox_dir[u'scl_max_dsbox'].setReadOnly(True)
        if self.cbox_dir[u'localOrWord_cbox'].isChecked() == True:
            self.cbox_dir[u'localOrWord_cbox'].setText(u'��ǰΪ�����ת')
        if self.cbox_dir[u'localOrWord_cbox'].isChecked() == False:
            self.cbox_dir[u'localOrWord_cbox'].setText(u'��ǰΪ������ת')

    def wnd_close(self):
        self.close()
        self.deleteLater()
        print '���߹رա�'


if __name__ == '__main__':
    try:
        a.wnd_close()
    except:
        pass

    a = PlaceObj()
    a.show()