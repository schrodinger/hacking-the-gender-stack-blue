from django.http import HttpResponse
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import SimilarityMaps
from IPython.display import SVG
import io
from PIL import Image
import numpy as np
import rdkit


class SimilarityMap(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="smiles",
                style="query",
            ),
            OpenApiParameter(
                name="smiles",
                style="query",
            ),
        ],
        responses={
            (200, "*/*"): OpenApiTypes.BYTE,
            (200, "applications/json"): OpenApiTypes.BYTE,
        },
    )
    def show_png(data):
        bio = io.BytesIO(data)
        img = Image.open(bio)
        return img

    def get(self, request):

        data = request.query_params
        data.is_valid(raise_exception=True)
        smiles1 = data[0].validated_data["smiles"]
        smiles2 = data[1].validated_data["smiles"]

        mol1 = Chem.MolFromSmiles(smiles1)
        mol2 = Chem.MolFromSmiles(smiles2)

        d = Draw.MolDraw2DCairo(400, 400)
        _, maxWeight = SimilarityMaps.GetSimilarityMapForFingerprint(
            mol1,
            mol2,
            lambda m, i: SimilarityMaps.GetMorganFingerprint(
                m, i, radius=2, fpType="bv"
            ),
            draw2d=d,
        )
        d.FinishDrawing()
        image = self.show_png(d.GetDrawingText())

        return HttpResponse(image, content_type="image/png")
