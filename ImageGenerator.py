import pylinac
from pylinac.core.image_generator import generate_picketfence, GaussianFilterLayer, PerfectFieldLayer, RandomNoiseLayer, Elekta_Iview
from pylinac.picketfence import Orientation

pf_file = "pf_teste_sem_erro.dcm"
generate_picketfence(
        simulator=Elekta_Iview(sid=1600),
        field_layer=PerfectFieldLayer,  # this applies a non-uniform intensity about the CAX, simulating the horn effect
        file_out=pf_file,
        final_layers=[
            #PerfectFieldLayer(field_size_mm=(5, 10), cax_offset_mm=(2.5, 90)),  # a 10mm gap centered over the picket
            #PerfectFieldLayer(field_size_mm=(5, 5), cax_offset_mm=(12.5, -87.5)),  # a 2.5mm extra opening of one leaf
            #PerfectFieldLayer(field_size_mm=(5, 5), cax_offset_mm=(22.5, -49)),  # a 1mm extra opening of one leaf
            GaussianFilterLayer(sigma_mm=1),
            RandomNoiseLayer(sigma=0.03)  # add salt & pepper noise
        ],
        pickets=9,
        picket_spacing_mm=20,
        picket_width_mm=6,  # wide-ish gap
        picket_height_mm=200, # Picket height parallel to leaf motion
        #orientation=Orientation.UP_DOWN,
)

pf_file = "pf_teste_erro1.dcm" # erro em 1 lamina
generate_picketfence(
        simulator=Elekta_Iview(sid=1600),
        field_layer=PerfectFieldLayer,  # this applies a non-uniform intensity about the CAX, simulating the horn effect
        file_out=pf_file,
        final_layers=[
            PerfectFieldLayer(field_size_mm=(10, 6), cax_offset_mm=(5, 1)),  # 1 mm de erro na lâmina 21 no picket central --> offset de 5 mm no y e 5 mm no x // field_size_mm=(y, x), cax_offset_mm=(y, x)
            PerfectFieldLayer(field_size_mm=(10, 6), cax_offset_mm=(-95, -42)),  # 2 mm de erro na lâmina 11 no picket central --> offset de 5 mm no y e 5 mm no x // field_size_mm=(y, x), cax_offset_mm=(y, x)
            GaussianFilterLayer(sigma_mm=1),
            RandomNoiseLayer(sigma=0.03)  # add salt & pepper noise
        ],
        pickets=9,
        picket_spacing_mm=20,
        picket_width_mm=6,  # wide-ish gap
        picket_height_mm=200, # Picket height parallel to leaf motion
        #orientation=Orientation.UP_DOWN,
)

'''
pf_file = "pf_teste_erro2.dcm" # picket offseT
generate_picketfence(
    simulator=Elekta_Iview(sid=1600),
    field_layer=PerfectFieldLayer,  # this applies a non-uniform intensity about the CAX, simulating the horn effect
    file_out=pf_file,
    final_layers=[
        GaussianFilterLayer(sigma_mm=1),
        RandomNoiseLayer(sigma=0.01)  # add salt & pepper noise
    ],
    pickets=5,
    picket_spacing_mm=20,
    picket_width_mm=5,
    picket_offset_error=[-5, 0, 0, 2, 0],  # array of errors; length must match the number of pickets === NAO FUNCIONA
    orientation=Orientation.UP_DOWN,
)


'''