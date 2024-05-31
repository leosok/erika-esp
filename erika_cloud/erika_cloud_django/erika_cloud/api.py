from ninja import NinjaAPI, Swagger, Router

# rewrite swagger to have try out button automatically enabled
api = NinjaAPI(csrf=True, title="Erika Cloud", version="1.0.0", docs=Swagger(settings={"tryItOutEnabled": True}))

router = Router()
# add health check endpoint
@router.get("/healthz")
def healthz(request):
    return {"status": "ok"}