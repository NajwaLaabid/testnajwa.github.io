class DotDictionary(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, *args, **kwargs):
        super(DotDictionary, self).__init__(*args, **kwargs)
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = DotDictionary(value)


## remove a certain percentage of grid connections
def remove_grid_connections(edge_index_clean, edge_attr_clean, flip_percentage):
    import torch
    edge_pairs = edge_index_clean.shape[-1] // 2
    num_to_remove = int(edge_pairs*flip_percentage)
    indices_to_remove = torch.randperm(edge_pairs)[:num_to_remove]
    keep_mask = torch.ones(edge_index_clean.shape[-1], dtype=torch.bool)
    keep_mask[indices_to_remove] = False
    keep_mask[indices_to_remove+1] = False
    edge_index_noisy = edge_index_clean[:, keep_mask]
    edge_attr_noisy = edge_attr_clean[keep_mask]
    return edge_index_noisy, edge_attr_noisy
