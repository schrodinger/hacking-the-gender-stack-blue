from django.http import HttpResponse
from rdkit.Chem import QED
from rdkit import Chem


class Proprieties(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="smiles",
                style="query",
            )
        ],
        responses={
            (200, "*/*"): OpenApiTypes.BYTE,
            (200, "applications/json"): OpenApiTypes.BYTE,
        },
    )
    def get(self, request):
        data = request.query_params
        data.is_valid(raise_exception=True)
        smiles = data.validated_data["smiles"]
        mol = Chem.MolFromSmiles(smiles)
        prop = QED.proprieties(mol)
        rule5 = prop[0] < 500 and prop[1] <= 5 and prop[2] <= 5 and prop[3] <= 10
        # convert prop
        propJSON = {
            "MW": prop[0],
            "ALOGP": prop[1],
            "HBD": prop[2],
            "HBA": prop[3],
            "PSA": prop[4],
            "ROTB": prop[5],
            "AROM": prop[6],
            "ALERTS": prop[7],
            "RULEOF5": rule5,
        }

        return HttpResponse(propJSON, content_type="applications/json")
