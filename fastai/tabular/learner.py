# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/43_tabular.learner.ipynb (unless otherwise specified).


from __future__ import annotations


__all__ = ['TabularLearner', 'tabular_learner']

# Cell
#nbdev_comment from __future__ import annotations
from ..basics import *
from .core import *
from .model import *
from .data import *

# Cell
class TabularLearner(Learner):
    "`Learner` for tabular data"
    def predict(self,
        row:pd.Series, # Features to be predicted
    ):
        "Predict on a single sample"
        dl = self.dls.test_dl(row.to_frame().T)
        dl.dataset.conts = dl.dataset.conts.astype(np.float32)
        inp,preds,_,dec_preds = self.get_preds(dl=dl, with_input=True, with_decoded=True)
        b = (*tuplify(inp),*tuplify(dec_preds))
        full_dec = self.dls.decode(b)
        return full_dec,dec_preds[0],preds[0]

# Cell
@delegates(Learner.__init__)
def tabular_learner(
        dls:TabularDataLoaders,
        layers:list=None, # Size of the layers generated by `LinBnDrop`
        emb_szs:list=None, # Tuples of `n_unique, embedding_size` for all categorical features
        config:dict=None, # Config params for TabularModel from `tabular_config`
        n_out:int=None, # Final output size of the model
        y_range:Tuple[float,float]=None, # Low and high for the final sigmoid function
        **kwargs
):
    "Get a `Learner` using `dls`, with `metrics`, including a `TabularModel` created using the remaining params."
    if config is None: config = tabular_config()
    if layers is None: layers = [200,100]
    to = dls.train_ds
    emb_szs = get_emb_sz(dls.train_ds, {} if emb_szs is None else emb_szs)
    if n_out is None: n_out = get_c(dls)
    assert n_out, "`n_out` is not defined, and could not be inferred from data, set `dls.c` or pass `n_out`"
    if y_range is None and 'y_range' in config: y_range = config.pop('y_range')
    model = TabularModel(emb_szs, len(dls.cont_names), n_out, layers, y_range=y_range, **config)
    return TabularLearner(dls, model, **kwargs)

# Cell
@typedispatch
def show_results(x:Tabular, y:Tabular, samples, outs, ctxs=None, max_n=10, **kwargs):
    df = x.all_cols[:max_n]
    for n in x.y_names: df[n+'_pred'] = y[n][:max_n].values
    display_df(df)