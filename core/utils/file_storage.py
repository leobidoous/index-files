import os
import uuid


def upload_to(instance, filename):
    folder = "notifications"

    if instance.__class__.__name__ == 'FirebaseModel':
        folder = "notifications"
    elif instance.__class__.__name__ == 'ServicesModel':
        folder = "services"
    elif instance.__class__.__name__ == 'IndividualPersonModel':
        folder = "individual_person"
    elif instance.__class__.__name__ == 'JuridicalPersonModel':
        folder = "juridical_person"

    return os.path.join('{}/{}'.format(folder, uuid.uuid4()))
