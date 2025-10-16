import csv
import pandas as pd
import math


def dump_meas_code(PointName, Xcoord, Zcoord, orientation=-1.0):
    PointMeasurementCode = """$$<MULTI_INSPECT name = "Groupe - {POINT}">
    GOTO/CART,{XCOORD},-11.05,{ZCOORD}
    $$<MEAS_POINT name = "{POINT}: 0.00,0.00,0.00, 0.00,{ORIENTATION},0.00">
    MODE/PROG,MAN
    F({POINT}=FEAT/POINT,CART,0,0,0,0,{ORIENTATION},0
    MEAS/POINT,F({POINT}),1
    PTMEAS/CART,{XCOORD},-2,{ZCOORD},0,{ORIENTATION},0
    ENDMES
    $$<\MEAS_POINT >
    $$<\MULTI_INSPECT = Groupe - {POINT}>"""
    return (PointMeasurementCode.format(POINT=PointName,XCOORD=Xcoord,ZCOORD=Zcoord, ORIENTATION=orientation))



def dump_measurement(points, ofile):
    for point in points:
        print(point['name'], point['x'], point['z'])
        PointName = point['name']
        Xcoord = point['x']
        Zcoord = point['z']
        ofile.write(dump_meas_code(PointName, Xcoord, Zcoord)+"\n\n")


def dump_plane_even(ofile, Xref, Yref, Zref, Orientation = -1, is6CP=False): #values to be cheked
    numbers = ["02","04","06","08","10","12"]
    code = """$$<CONSTRUCT_PLANE name = "PLN_Module_{NUMBER}F = Assistant pour la construction:  A{NUMBER}$
    F1 - A{NUMBER}F2 - A{NUMBER}F3 - A{NUMBER}F4 - A{NUMBER}F5 - B{NUMBER}F1- B{NUMBER}F2 - B{NUMBER}F3 - B{NUMBER}F4 - C{NUMBER}F1- C{NUMBER}$
    F2 - C{NUMBER}F3 - C{NUMBER}F4 - C{NUMBER}F5 - D{NUMBER}F1- D{NUMBER}F2 - D{NUMBER}F3 - D{NUMBER}F4 - D{NUMBER}F5"""
    if is6CP:
        code+="- E{NUMBER}F1 - E{NUMBER}F2 - E{NUMBER}F3 - E{NUMBER}F4$"""
    code+="""- F{NUMBER}F1 - F{NUMBER}$
    F2 - F{NUMBER}F3 - F{NUMBER}F4 - F{NUMBER}F5">
    F(PLN_Module_{NUMBER}F)=FEAT/PLANE,CART,{XREF},{YREF},{ZREF},0,{ORIENTATION},0
    CONST/PLANE,F(PLN_Module_{NUMBER}F),BF,FA(A{NUMBER}F1),FA(A{NUMBER}F2),FA(A{NUMBER}F3),FA(A02F4),FA(A02$
    F5),FA(B02F1),FA(B{NUMBER}F2),FA(B{NUMBER}F3),FA(B{NUMBER}F4),FA(C{NUMBER}F1),FA(C{NUMBER}F2),FA(C{NUMBER}F3),FA(C0$
    2F4),FA(C{NUMBER}F5),FA(D{NUMBER}F1),FA(D{NUMBER}F2),FA(D{NUMBER}F3),FA(D{NUMBER}F4),FA(D{NUMBER}F5),"""
    if is6CP:
        code+="FA(E{NUMBER}F1),FA(E{NUMBER}F2),FA(E{NUMBER}F3),FA(E{NUMBER}F4),FA(E{NUMBER}F4)"
    code+="""FA(F{NUMBER}F1),FA(F$
    {NUMBER}F2),FA(F{NUMBER}F3),FA(F{NUMBER}F4),FA(F{NUMBER}F5)
    $$<\CONSTRUCT_PLANE >
    T(PLN_Module_{NUMBER}F)=TOL/FLAT,0.1
    OUTPUT/FA(PLN_Module_{NUMBER}F),TA(PLN_Module_{NUMBER}F)"""

    for number in numbers:
        ofile.write(code.format(NUMBER=number, XREF=Xref, YREF=Yref, ZREF=Zref, ORIENTATION=Orientation)+"\n\n")    


def dump_distance_sphere(points, ofile):
    for point in points:
        PointName = point['name']   
        ofile.write(f"""OUTPUT/FA({PointName}),TA(Dist)\n""")


def dump_distance_pnt7(point, ofile):
    for point in points:
        PointName = point['name']   
        ofile.write(f"""OUTPUT/FA({PointName}),FA(PNT007_Décalé),TA(Dist)\n""")    


def dump_distance_line(points, ofile):
    for point in points:
        PointName = point['name']
        ofile.write(f"""OUTPUT/FA({PointName}),FA(LINE001),TA(Dist)\n""")

if __name__ == "__main__":


    # Read the point coordinates for module 2
    df = pd.read_csv("Odd_coord.csv", delimiter=';')
    data = df.to_dict(orient="records")  # list of dicts
    #print(data)
    Points02 = []
    for row in data:
        Points02.append({'name':row['Point']+"02F1", 'x':row['X1'], 'z':row['Z1'], 'orientation':-1.0})
        Points02.append({'name':row['Point']+"02F2", 'x':row['X2'], 'z':row['Z2'], 'orientation':-1.0})
        Points02.append({'name':row['Point']+"02F3", 'x':row['X3'], 'z':row['Z3'], 'orientation':-1.0})
        Points02.append({'name':row['Point']+"02F4", 'x':row['X4'], 'z':row['Z4'], 'orientation':-1.0})
        if not math.isnan(row['X5']):
            Points02.append({'name':row['Point']+"02F5", 'x':row['X5'], 'z':row['Z5'], 'orientation':-1.0})

    print(Points02 )

    # Read the distances betweem odd modules
    df = pd.read_csv("Odd_dist.csv", delimiter=';')
    print(df)
    Dist_odd = []
    Dist_odd.append({"number":"04","offset":-df["04"][0]})
    Dist_odd.append({"number":"06","offset":-df["04"][0]-df["06"][0]})
    Dist_odd.append({"number":"08","offset":-df["04"][0]-df["06"][0]-df["08"][0]})
    Dist_odd.append({"number":"10","offset":-df["04"][0]-df["06"][0]-df["08"][0]-df["10"][0]})
    Dist_odd.append({"number":"12","offset":-df["04"][0]-df["06"][0]-df["08"][0]-df["10"][0]-df["12"][0]})
    print(Dist_odd)

    # Generate points for all inserts
    points = []
    # add all points of 02
    for point in Points02:
        points.append(point)
    #points = Points02
    for dist in Dist_odd:
        for point in Points02:
            points.append({'name':point['name'][0]+dist['number']+point['name'][2:], 'x':point['x'], 'z':float(point['z'])+float(dist['offset'])})#, 'orientation':point['orientation']})
     
    print(points)
    #exit()
     
    #points = [
    #    {'name': 'A02F1', 'x': 100.0, 'z': 200.0, 'orientation': -1.0},
    #    {'name': 'A02F2', 'x': 150.0, 'z': 250.0, 'orientation': -1.0}
    #]
    ofile = open("mmt_code.dmi", "w")

    #copy the header
    ifile = open("header.dmi",'r')
    ofile.write(ifile.read())
    ifile.close()

    dump_measurement(points, ofile)
    
    #break
    ofile.write("MODE/AUTO,PROG,MAN \nGOTO/CART,13,-54,28\nGOTO/CART,13,-54,400\n\n$$PAUSE\n")
    
    #compute distance to sphere
    ofile.write("T(Dist)=TOL/DISTWRT,NOMINL,2.175,-0.12,0.12,FA(PLN_SphËres),YAXIS,AVG\n\n")
    dump_distance_sphere(points, ofile)

    #compute distance to PNT007
    dump_distance_pnt7(points, ofile)
    ofile.write("T(Dist)=TOL/DISTB,NOMINL,10,-0.12,0.12,XAXIS,AVG\n\n")
    
    #compute distance to line
    ofile.write("T(Dist)=TOL/DISTB,NOMINL,0,-0.1,0.1,ZAXIS,AVG\n\n")
    dump_distance_line(points, ofile)


    #plane dump_measurement for even modules
    #dump_plane_even(ofile, Xref=1013.917, Yref=-2, Zref=81.617,0, Orientation=-1, is6CP=True)

    ofile.close()
