from abc import ABC
from typing import Tuple

import numpy as np
from pydicom.dataset import Dataset, FileMetaDataset
from pydicom.uid import generate_uid
import datetime

from pylinac.core.image_generator.layers import Layer


class Simulator(ABC):
    """Abstract class for an image simulator"""
    pixel_size: float
    shape: Tuple[int, int]

    def __init__(self, sid: float = 1500):
        """

        Parameters
        ----------
        sid
            Source to image distance in mm.
        """
        self.image = np.zeros(self.shape, np.uint16)
        self.sid = sid
        self.mag_factor = sid / 1000

    def add_layer(self, layer: Layer) -> None:
        """Add a layer to the image"""
        self.image = layer.apply(self.image, self.pixel_size, self.mag_factor)

    def generate_dicom(self, file_out_name: str, **kwargs):
        """Generate a DICOM file with the constructed image (via add_layer)"""
        raise NotImplementedError("This method has not been implemented for this simulator. Overload the method of your simulator.")


class AS500Image(Simulator):
    """Simulates an AS500 EPID image."""
    pixel_size: float = 0.78125
    shape: Tuple[int, int] = (384, 512)

    def generate_dicom(self, file_out_name: str, gantry_angle: float = 0.0, coll_angle: float = 0.0,
                       table_angle: float = 0.0) -> None:
        # make image look like an EPID with flipped data (dose->low)
        flipped_image = -self.image + self.image.max() + self.image.min()

        file_meta = FileMetaDataset()
        # Main data elements
        ds = Dataset()
        ds.ImageType = ['DERIVED', 'SECONDARY', 'PORTAL']
        ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.481.1'
        ds.SOPInstanceUID = '1.2.840.113854.141883099300381770008774160544352783139.1.1'
        ds.StudyDate = '20150212'
        ds.ContentDate = '20150212'
        ds.StudyTime = '124120'
        ds.ContentTime = '124120'
        ds.AccessionNumber = ''
        ds.Modality = 'RTIMAGE'
        ds.ConversionType = 'WSD'
        ds.Manufacturer = 'IMPAC Medical Systems, Inc.'
        ds.ReferringPhysicianName = ''
        ds.StudyDescription = 'QA'
        ds.SeriesDescription = 'D + Gantry_0'
        ds.PhysiciansOfRecord = 'Awesome Physician'
        ds.OperatorsName = ''
        ds.ManufacturerModelName = 'MOSAIQ'
        ds.PatientName = 'Lutz^Test Tool'
        ds.PatientID = 'zzzBAC_Lutz'
        ds.PatientBirthDate = ''
        ds.SoftwareVersions = '2.41.01J0'
        ds.StudyInstanceUID = '1.2.840.113854.141883099300381770008774160544352783139'
        ds.SeriesInstanceUID = '1.2.840.113854.141883099300381770008774160544352783139.1'
        ds.StudyID = '348469'
        ds.SeriesNumber = "4597199"
        ds.InstanceNumber = "0"
        ds.PatientOrientation = ''
        ds.PositionReferenceIndicator = ''
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = 'MONOCHROME2'
        ds.Rows = self.image.shape[0]
        ds.Columns = self.image.shape[1]
        ds.BitsAllocated = 16
        ds.BitsStored = 16
        ds.HighBit = 15
        ds.PixelRepresentation = 0
        ds.RTImageLabel = 'D'
        ds.RTImagePlane = 'NORMAL'
        ds.XRayImageReceptorAngle = "0.0"
        ds.ImagePlanePixelSpacing = [self.pixel_size, self.pixel_size]
        ds.RTImagePosition = [-200.70400, 150.52800]
        ds.RadiationMachineSAD = "1000.0"
        ds.RTImageSID = self.sid
        ds.PrimaryDosimeterUnit = 'MU'
        ds.GantryAngle = str(gantry_angle)
        ds.BeamLimitingDeviceAngle = str(coll_angle)
        ds.PatientSupportAngle = str(table_angle)
        ds.PixelData = flipped_image  # XXX Array of 393216 bytes excluded

        ds.file_meta = file_meta
        ds.is_implicit_VR = True
        ds.is_little_endian = True
        ds.save_as(file_out_name, write_like_original=False)


class AS1000Image(Simulator):
    """Simulates an AS1000 EPID image."""
    pixel_size: float = 0.390625
    shape: Tuple[int, int] = (768, 1024)

    def generate_dicom(self, file_out_name: str, gantry_angle: float = 0.0, coll_angle: float = 0.0,
                       table_angle: float = 0.0) -> None:
        # make image look like an EPID with flipped data (dose->low)
        flipped_image = -self.image + self.image.max() + self.image.min()

        # File meta info data elements
        file_meta = FileMetaDataset()

        # Main data elements
        ds = Dataset()
        ds.ImageType = ['DERIVED', 'SECONDARY', 'PORTAL']
        ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.481.1'
        ds.SOPInstanceUID = '1.2.840.113854.323870129946883845737820671794195198978.1.1'
        ds.StudyDate = '20140819'
        ds.ContentDate = '20140819'
        ds.StudyTime = '130944'
        ds.ContentTime = '130944'
        ds.AccessionNumber = ''
        ds.Modality = 'RTIMAGE'
        ds.ConversionType = 'WSD'
        ds.Manufacturer = 'IMPAC Medical Systems, Inc.'
        ds.ReferringPhysicianName = ''
        ds.StudyDescription = 'QA'
        ds.SeriesDescription = 'Q + Couch_270'
        ds.PhysiciansOfRecord = 'I am king'
        ds.OperatorsName = ''
        ds.ManufacturerModelName = 'MOSAIQ'
        ds.PatientName = 'Albert Einstein'
        ds.PatientID = 'abc123'
        ds.PatientBirthDate = ''
        ds.SoftwareVersions = '2.41.01J0'
        ds.StudyInstanceUID = '1.2.840.113854.323870129946883845737820671794195198978'
        ds.SeriesInstanceUID = '1.2.840.113854.323870129946883845737820671794195198978.1'
        ds.StudyID = '348469'
        ds.SeriesNumber = "4290463"
        ds.InstanceNumber = "0"
        ds.PatientOrientation = ''
        ds.PositionReferenceIndicator = ''
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = 'MONOCHROME2'
        ds.Rows = self.shape[0]
        ds.Columns = self.shape[1]
        ds.BitsAllocated = 16
        ds.BitsStored = 16
        ds.HighBit = 15
        ds.PixelRepresentation = 0
        ds.RTImageLabel = 'Q'
        ds.RTImagePlane = 'NORMAL'
        ds.XRayImageReceptorAngle = "0.0"
        ds.ImagePlanePixelSpacing = [self.pixel_size, self.pixel_size]
        ds.RTImagePosition = [-200.70400, 150.523400]
        ds.RadiationMachineSAD = "1000.0"
        ds.RTImageSID = self.sid
        ds.PrimaryDosimeterUnit = 'MU'
        ds.GantryAngle = str(gantry_angle)
        ds.BeamLimitingDeviceAngle = str(coll_angle)
        ds.PatientSupportAngle = str(table_angle)
        # ds.CurveDimensions = 2
        # ds.NumberOfPoints = 4
        # ds.TypeOfData = 'ROI'
        # ds.CurveDescription = 'VContour 30'
        # ds.AxisUnits = ['PIXL', 'PIXL']
        # ds.DataValueRepresentation = 3
        # ds.CurveLabel = 'Field Edge (Q:MV)'
        # ds.CurveData = b'\x00\x00\x00\x00 .\x81@\x00\x00\x00\x00\x10\\z@\x00\x00\x00\x00 .\x81@\x00\x00\x00\x00\x90\x93u@\x00\x00\x00\x00\xc0\x93}@\x00\x00\x00\x00\x90\x93u@\x00\x00\x00\x00\xc0\x93}@\x00\x00\x00\x00\x10\\z@'
        ds.PixelData = flipped_image  # XXX Array of 1572864 bytes excluded

        ds.file_meta = file_meta
        ds.is_implicit_VR = True
        ds.is_little_endian = True
        ds.save_as(file_out_name, write_like_original=False)


class AS1200Image(Simulator):
    """Simulates an AS1200 EPID image."""
    pixel_size: float = 0.336
    shape: Tuple[int, int] = (1280, 1280)

    def generate_dicom(self, file_out_name: str, gantry_angle: float = 0.0, coll_angle: float = 0.0,
                       table_angle: float = 0.0) -> None:
        file_meta = FileMetaDataset()
        file_meta.FileMetaInformationGroupLength = 196
        file_meta.FileMetaInformationVersion = b'\x00\x01'
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.481.1'
        file_meta.MediaStorageSOPInstanceUID = '1.2.246.352.64.1.5468686515961995030.4457606667843517571'
        file_meta.TransferSyntaxUID = '1.2.840.10008.1.2'
        file_meta.ImplementationClassUID = '1.2.246.352.70.2.1.120.1'
        file_meta.ImplementationVersionName = 'MergeCOM3_410'

        # Main data elements
        ds = Dataset()
        ds.SpecificCharacterSet = 'ISO_IR 100'
        ds.ImageType = ['ORIGINAL', 'PRIMARY', 'PORTAL']
        ds.InstanceCreationDate = '20161230'
        ds.InstanceCreationTime = '215510'
        ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.481.1'
        ds.SOPInstanceUID = '1.2.246.352.64.1.5468686515961995030.4457606667843517571'
        ds.StudyDate = '20161230'
        ds.ContentDate = '20161230'
        ds.StudyTime = '215441.936'
        ds.ContentTime = '215441.936'
        ds.AccessionNumber = ''
        ds.Modality = 'RTIMAGE'
        ds.ConversionType = ''
        ds.Manufacturer = 'Varian Medical Systems'
        ds.ReferringPhysicianName = ''
        ds.StationName = 'NDS-WKS-SN9999'
        ds.OperatorsName = 'King Kong'
        ds.ManufacturerModelName = 'VMS.XI.Service'
        ds.PatientName = 'Grace Hopper'
        ds.PatientID = 'VMS.XI.Service'
        ds.PatientBirthDate = '19000101'
        ds.PatientBirthTime = '000000'
        ds.PatientSex = ''
        ds.SoftwareVersions = '2.5.13.2'
        ds.StudyInstanceUID = '1.2.246.352.64.4.5644626269434644263.1905029945372990626'
        ds.SeriesInstanceUID = '1.2.246.352.64.2.5508761605912087323.11665958260371685307'
        ds.StudyID = 'fdd794f2-8520-4c4a-aecc-e4446c1730ff'
        ds.SeriesNumber = None
        ds.AcquisitionNumber = "739774555"
        ds.InstanceNumber = "1"
        ds.PatientOrientation = ''
        ds.FrameOfReferenceUID = '1.2.246.352.64.3.4714322356925391886.9391210174715030407'
        ds.PositionReferenceIndicator = ''
        ds.SamplesPerPixel = 1
        ds.PhotometricInterpretation = 'MONOCHROME1'
        ds.PlanarConfiguration = 0
        ds.Rows = self.shape[0]
        ds.Columns = self.shape[1]
        ds.BitsAllocated = 16
        ds.BitsStored = 16
        ds.HighBit = 15
        ds.PixelRepresentation = 0
        ds.WindowCenter = "32767.0"
        ds.WindowWidth = "65535.0"
        ds.RescaleIntercept = "0.0"
        ds.RescaleSlope = "1.0"
        ds.RescaleType = 'US'
        ds.RTImageLabel = 'MV_180'
        ds.RTImageDescription = ""
        ds.ReportedValuesOrigin = 'ACTUAL'
        ds.RTImagePlane = 'NORMAL'
        ds.XRayImageReceptorTranslation = [0.00, 0.00, 1000 - self.sid]
        ds.XRayImageReceptorAngle = "0.0"
        ds.RTImageOrientation = [1, 0, 0, 0, -1, 0]
        ds.ImagePlanePixelSpacing = [self.pixel_size, self.pixel_size]
        ds.RTImagePosition = [-214.872, 214.872]
        ds.RadiationMachineName = 'TrueBeam from Hell'
        ds.RadiationMachineSAD = "1000.0"
        ds.RTImageSID = self.sid
        ds.PrimaryDosimeterUnit = 'MU'
        ds.GantryAngle = str(gantry_angle)
        ds.BeamLimitingDeviceAngle = str(coll_angle)
        ds.PatientSupportAngle = str(table_angle)
        ds.TableTopVerticalPosition = "-24.59382842824"
        ds.TableTopLongitudinalPosition = "200.813502948597"
        ds.TableTopLateralPosition = "3.00246706215532"
        ds.PixelData = self.image  # XXX Array of 3276800 bytes excluded

        ds.file_meta = file_meta
        ds.is_implicit_VR = True
        ds.is_little_endian = True
        ds.save_as(file_out_name, write_like_original=False)


class Elekta_Iview(Simulator): # Add by William Santos - william.wapsantos@gmail.com
    """Simulates an Elekta Iview image."""
    pixel_size: float = 0.4
    shape: Tuple[int, int] = (1024, 1024)

    def generate_dicom(self, file_out_name: str, gantry_angle: float = 0.0, coll_angle: float = 0.0,
                       table_angle: float = 0.0) -> None:
        file_meta = FileMetaDataset()

        instance_uid = generate_uid(prefix='1.2.826.0.1.3680043.10.565.')

        #Create files with minimum information
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.481.1' #http://dicom.nema.org/dicom/2013/output/chtml/part04/sect_I.4.html
        file_meta.MediaStorageSOPInstanceUID = instance_uid


        # Main data elements
        ds = Dataset()
        ds.SpecificCharacterSet = 'ISO_IR 100'
        ds.ImageType = ['ORIGINAL', 'PRIMARY', 'PORTAL']
        #Add creation date and time
        dt = datetime.datetime.now()
        ds.ContentDate = dt.strftime('%Y%m%d')
        timeStr = dt.strftime('%H%M%S.%f') 
        ds.ContentTime = timeStr

        ds.add_new([0x0008,0x0016], 'UI', '1.2.840.10008.5.1.4.1.1.481.1') #SOP Class UID
        ds.add_new([0x0008,0x0018], 'UI', instance_uid) #SOP Instance UID
        ds.add_new([0x0028,0x0010], 'US', self.shape[0]) #rows
        ds.add_new([0x0028,0x0011], 'US', self.shape[1]) #columns
        ds.add_new([0x0028,0x0100], 'US', 16) #Bits Alocated
        ds.add_new([0x0028,0x0103], 'US', 0) # PixelRepresentation
        ds.add_new([0x0028,0x0002], 'US', 1) # SamplesPerPixel
        ds.add_new([0x0028,0x0004], 'CS', 'MONOCHROME2') # Photometric Interpretation ==> https://dicom.innolitics.com/ciods/enhanced-mr-image/enhanced-mr-image/00280103
        ds.add_new([0x0008,0x0060], 'CS', 'RTIMAGE') #Modality
        ds.add_new([0x0028,0x0101], 'US', 16) #Bits Stored
        ds.add_new([0x0028,0x0102], 'US', 15) #High Bit ==> https://dicom.innolitics.com/ciods/us-image/image-pixel/00280102
        ds.add_new([0x3002,0x0022], 'DS', '1000.0') # Radiation Machine SAD
        ds.add_new([0x3002,0x0026], 'DS', self.sid) # RT Image SID
        ds.add_new([0x5000,0x0030], 'SH', ['PIXL', 'PIXL']) #Axis Units
        ds.add_new([0x3002,0x0011], 'DS', [self.pixel_size, self.pixel_size]) #Image Plane Pixel Spacing
        ds.add_new([0x3002,0x000D], 'DS', [0.0, 0.0]) # X-Ray Image Receptor Translation Attribute ==> https://dicom.innolitics.com/ciods/rt-beams-delivery-instruction/rt-beams-delivery-instruction/00741020/00741030/3002000d
        ds.add_new([0x300A,0x011E], 'DS', '0.0')# Gantry Angle
        ds.add_new([0x300A,0x0120], 'DS', '0.0')# Beam Limiting Device (Colimator) Angle
        ds.add_new([0x300A,0x0122], 'DS', '0.0')# Patient Support Angle (mesa)
        ds.PixelData = self.image  # XXX Array of 3276800 bytes excluded

        ds.file_meta = file_meta
        ds.is_implicit_VR = True
        ds.is_little_endian = True
        ds.save_as(file_out_name, write_like_original=False)
