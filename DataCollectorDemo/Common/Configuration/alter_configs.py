from Common.Communication import ConfigurationModel

def join_configs(config1: ConfigurationModel, config2: ConfigurationModel, set_one_dominant: bool = True):
    new_dict = {}
    cm1, cm2 = (config1, config2) if set_one_dominant else (config2, config1)

    for key, value in cm2:
        new_dict[key] = value

    for key, value in cm1:
        new_dict[key] = value

    new_config = ConfigurationModel(entries=new_dict)

    return new_config
