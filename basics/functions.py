
# GET AND GENERATE AUTO ID FROM MODELS
def get_auto_id(model):
    auto_id = 1
    latest_auto_id = model.objects.all().order_by("-created_at")[:1]
    if latest_auto_id:
        for auto in latest_auto_id:
            auto_id = auto.auto_id + 1
    return auto_id
