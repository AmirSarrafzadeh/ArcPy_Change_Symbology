import os
import arcpy
import logging

if __name__ == '__main__':

    # The logging setting has done
    logging.basicConfig(filename="file.log",
                        level=logging.INFO,
                        format='%(levelname)s   %(asctime)s   %(message)s')
    logging.info("All setting of the logging is done")

    # Set all the paths
    path = os.getcwd()
    aprx_path = os.path.join(path, "ArcGIS\Project_01\Project_01.aprx")
    gdb_path = os.path.join(path, "ACC.gdb")
    symbology_path = os.path.join(path, "Symbology")
    logging.info("All paths are defined")

    # Read aprx project
    if arcpy.Exists(aprx_path):
        aprx_project = arcpy.mp.ArcGISProject(aprx_path)
        logging.info("aprx project is read")
    else:
        logging.error("aprx project is not exist")

    # Select the first map
    map_1 = aprx_project.listMaps()[0]

    # Set the path of the gdb as environment
    arcpy.env.workspace = gdb_path

    # Select all the symbologies inside the directory
    symbology_list = []
    symbology_list = [item.split(".")[0] for item in os.listdir(symbology_path)]

    list_layers = map_1.listLayers()
    layer_names = [layer.name for layer in list_layers]
    fclist = arcpy.ListFeatureClasses()

    for fc in fclist:
        if fc not in layer_names and fc in symbology_list:
            lay = gdb_path + os.sep + fc
            map_1.addDataFromPath(lay)
            logging.info(f"{fc} is added to the map")

    for i in range(len(map_1.listLayers())):
        for j in symbology_list:
            if map_1.listLayers()[i].name == j:
                lyrx_path = symbology_path + os.sep + j + ".lyrx"
                arcpy.management.ApplySymbologyFromLayer(map_1.listLayers()[i],
                                                         lyrx_path,
                                                         None, "DEFAULT")
                logging.info(f"symbology of the {j} is changed")

    aprx_project.save()
    logging.info("Project is saved")
