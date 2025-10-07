def model(dbt, session):
    dbt.config(
        submission_method="bigframes",
        notebook_template_id='8573503490234515456',
    )

    data = {'id': [0, 1, 3],'name': ['Brian', 'Isaac', 'Marie']}
    return bpd.DataFrame(data)