# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------------

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import copy
import numpy as np
import matplotlib.pyplot as plt
import json

# ---------------------------------------------------------------------------

col = plt.rcParams['axes.prop_cycle'].by_key()['color']

def fill_color(hex, opacity):
    hex = hex.lstrip('#')
    hlen = len(hex)
    return 'rgba' + str(tuple([int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3)] + [opacity]))

fcol = [fill_color(c, 0.5) for c in col]

# ---------------------------------------------------------------------------

fname = './json/stations.json'
with open(fname, 'r') as f:
    stations = json.load(f)

# iso_id = '8447930'
# stations = {iso_id: stations[iso_id]}

station_list = [{'label': stations[s]['name'], 'value': s} for s in stations]
station_list = sorted(station_list, key=lambda k: k['label'])

fname = './json/thresholds.json'
with open(fname, 'r') as f:
    thresholds = json.load(f)

fname = './json/projection_years.json'
with open(fname, 'r') as f:
    prjn_yrs = json.load(f)
dec_yrs = [y -4 for y in prjn_yrs[9:-1:10]]
dec_lmslr_drpdwn = [{'label': 'NOAA Intermediate Low', 'value': 'int_low'}, {'label': 'NOAA Intermediate', 'value': 'int'}, {'label': 'NOAA Intermediate High', 'value': 'int_high'}, {'label': 'Kopp et al. (2014) RCP8.5', 'value': 'kopp'}]

fname = './json/first_year_counts.json'
with open(fname, 'r') as f:
    fyr_cnts = json.load(f)
fyr_cnts_drpdwn = [{'label':n, 'value':n} for n in fyr_cnts]

# ---------------------------------------------------------------------------
# initialize

fyrc_init = str(50)
uid_init = '8658120'

fname = './json/' + uid_init + '/' + 'thresholds.json'
with open(fname, 'r') as f:
    noaa_thrsh_init = json.load(f)
slider_thrsh_init = '{:0>3}'.format(int(noaa_thrsh_init['minor']))

fname = './json/' + uid_init + '/' \
    + slider_thrsh_init + '/' + 'projections.json'
with open(fname, 'r') as f:
    prjn_init = json.load(f)

fname = './json/' + uid_init + '/' + slider_thrsh_init + '/' + 'first_years.json'
with open(fname, 'r') as f:
    fyrs_init = json.load(f)

fname = './json/' + uid_init + '/' + slider_thrsh_init + '/' + 'occ_to_chrnc.json'
with open(fname, 'r') as f:
    o2c_init = json.load(f)

dec_lmslr_init = 'int'

fname = './json/' + uid_init + '/' + slider_thrsh_init + '/' + 'dec_total.json'
with open(fname, 'r') as f:
    dtot = json.load(f)
    dtot_init = dtot[dec_lmslr_init]

fname = './json/' + uid_init + '/' + slider_thrsh_init + '/' + 'dec_max.json'
with open(fname, 'r') as f:
    dmax = json.load(f)
    dmax_init = dmax[dec_lmslr_init]

# ---------------------------------------------------------------------------

def noaa_traces(data):
    return [

        # -------------------------------------------------------------------
        # intermediate high

        {'x': prjn_yrs, 'y': data['int_high']['17'], 'type': 'scatter', 'fill': 'none', 'showlegend': False, 'line': {'color': fcol[3], 'width': 0}, 'hoverinfo': 'x+y'},

        {'x': prjn_yrs, 'y': data['int_high']['83'], 'type': 'scatter', 'fill': 'tonexty', 'fillcolor': fcol[3], 'opacity': 0.5, 'name': 'NOAA Interm. High', 'mode': 'none', 'hoverinfo': 'x+y'},

        {'x': prjn_yrs, 'y': data['int_high']['50'], 'type': 'scatter', 'mode': 'lines', 'showlegend': False, 'line': {'color': col[3]}, 'hoverinfo': 'x+y'},

        # -------------------------------------------------------------------
        # intermediate low

        {'x': prjn_yrs, 'y': data['int_low']['17'], 'type': 'scatter', 'fill': 'none', 'showlegend': False, 'line': {'color': fcol[0], 'width': 0}, 'hoverinfo': 'x+y'},

        {'x': prjn_yrs, 'y': data['int_low']['83'], 'type': 'scatter', 'fill': 'tonexty', 'fillcolor': fcol[0], 'name': 'NOAA Interm. Low', 'mode': 'none', 'hoverinfo': 'x+y'},

        {'x': prjn_yrs, 'y': data['int_low']['50'], 'type': 'scatter', 'showlegend': False, 'line': {'color': col[0]}, 'hoverinfo': 'x+y'},

        # -------------------------------------------------------------------
        # intermediate

        {'x': prjn_yrs, 'y': data['int']['17'], 'type': 'scatter', 'fill': 'none', 'showlegend': False, 'line': {'color': fcol[1], 'width': 0}, 'hoverinfo': 'x+y'},

        {'x': prjn_yrs, 'y': data['int']['83'], 'type': 'scatter', 'fill': 'tonexty', 'fillcolor': fcol[1], 'name': 'NOAA Intermediate', 'mode': 'none', 'hoverinfo': 'x+y'},

        {'x': prjn_yrs, 'y': data['int']['50'], 'type': 'scatter', 'showlegend': False, 'line': {'color': col[1]}, 'hoverinfo': 'x+y'},

    ]

# ---------------------------------------------------------------------------

def kopp_traces(data):
    return [

        # -------------------------------------------------------------------
        # Kopp et al. (2014) RCP8.5

        {'x': prjn_yrs, 'y': data['kopp']['5'], 'type': 'scatter', 'fill': 'none', 'showlegend': False, 'line': {'color': fill_color(col[4], 0.33), 'width': 0}, 'hoverinfo': 'y'},

        {'x': prjn_yrs, 'y': data['kopp']['17'], 'type': 'scatter', 'fill': 'tonexty', 'fillcolor': fill_color(col[4], 0.33), 'line': {'color': fill_color(col[4], 0.67), 'width': 0}, 'showlegend': False, 'hoverinfo': 'y'},

        {'x': prjn_yrs, 'y': data['kopp']['83'], 'type': 'scatter', 'fill': 'tonexty', 'fillcolor': fill_color(col[4], 0.67), 'name': 'Likely (17-83%)', 'mode': 'none', 'hoverinfo': 'y'},

        {'x': prjn_yrs, 'y': data['kopp']['95'], 'type': 'scatter', 'fill': 'tonexty', 'fillcolor': fill_color(col[4], 0.33), 'name': 'Very likely (5-95%)', 'mode': 'none', 'hoverinfo': 'y'},

        {'x': prjn_yrs, 'y': data['kopp']['50'], 'type': 'scatter', 'name': 'Median', 'line': {'color': col[4], 'width': 3}, 'hoverinfo': 'y'},

    ]

# ---------------------------------------------------------------------------

def firstyear_traces(data, fyrc):

    y0 = {'int_low': 2.5, 'int': 3.5, 'int_high': 4.5, 'kopp': 1.5}
    base_col = {'int_low': col[0], 'int': col[1], 'int_high': col[3], 'kopp': col[4]}

    traces = []

    for ii, scn in enumerate(data):
        pctl_yrs = data[scn][fyrc]
        pctl = list(pctl_yrs.keys())
        o = np.linspace(0, 1, len(pctl)+1)[1:-1]
        opcty = {pctl[k]: o[k] for k in range(len(o))}
        for p1, p2 in zip(pctl[:-1], pctl[1:]):
            x = [pctl_yrs[p2], pctl_yrs[p1], pctl_yrs[p1], pctl_yrs[p2]]
            y = [y0[scn]+0.9, y0[scn]+0.9, y0[scn]+0.1, y0[scn]+0.1]
            traces.append(
                {'x': x, 'y': y, 'fill': 'toself', 'fillcolor': fill_color(base_col[scn], opcty[p1]), 'mode': 'none'}
            )

            x = [pctl_yrs[p1], pctl_yrs[p1]]
            y = [y0[scn]+0.9, y0[scn]+0.1]
            if p1 == '50':
                traces.append(
                    {'x': x, 'y': y, 'mode': 'lines', 'line': {'color': '#000000', 'width': 3}, 'text': p1 + '% probability', 'hoverinfo': 'x+text'}
                )
            else:
                traces.append(
                    {'x': x, 'y': y, 'mode': 'lines', 'line': {'color': fill_color(base_col[scn], opcty[p1]), 'width': 0.5}, 'text': p1 + '% probability', 'hoverinfo': 'x+text'}
                )
            if p2 == pctl[-1]:
                x = [pctl_yrs[p2], pctl_yrs[p2]]
                y = [y0[scn]+0.9, y0[scn]+0.1]
                traces.append(
                    {'x': x, 'y': y, 'mode': 'lines', 'line': {'color': fill_color(base_col[scn], opcty[p1]), 'width': 1}, 'text': p2 + '% probability', 'hoverinfo': 'x+text'}
                )

        for jj, p1 in enumerate(pctl[:-1]):
            x = [jj+1, jj, jj, jj+1]
            y = [y0[scn]+1.0, y0[scn]+1.0, y0[scn]+0.0, y0[scn]+0.0]
            traces.append(
                {'x': x, 'y': y, 'fill': 'toself', 'fillcolor': fill_color(base_col[scn], opcty[p1]), 'mode': 'none', 'xaxis': 'x2', 'yaxis': 'y2', 'hoverinfo': 'none'}
            )
            if p1 == '50':
                x = [jj, jj]
                y = [y0[scn]+1.0, y0[scn]+0.0]
                traces.append(
                    {'x': x, 'y': y, 'mode': 'lines', 'line': {'color': '#000000', 'width': 3}, 'xaxis': 'x2', 'yaxis': 'y2', 'hoverinfo': 'none'}
                )

    return traces

# ---------------------------------------------------------------------------

def occ2chrnc_traces(data):

    y0 = {'int_low': 2.5, 'int': 3.5, 'int_high': 4.5, 'kopp': 1.5}
    base_col = {'int_low': col[0], 'int': col[1], 'int_high': col[3], 'kopp': col[4]}

    traces = []

    for ii, scn in enumerate(data):

        x1 = data[scn]['occ']['50']
        x2 = data[scn]['chrnc']['50']
        x = [x2, x1, x1, x2]
        y = [y0[scn]+0.9, y0[scn]+0.9, y0[scn]+0.1, y0[scn]+0.1]
        traces.append(
            {'x': x, 'y': y, 'fill': 'toself', 'fillcolor': fill_color(base_col[scn], 0.5), 'mode': 'none', 'hoverinfo': 'none'}
        )

        dy0 = 0.125 if data[scn]['chrnc']['17'] < data[scn]['occ']['83'] else 0
        for oc in data[scn]:
            dy = dy0 if oc == 'chrnc' else -dy0
            for p in ['17', '83']:
                x = [data[scn][oc][p], data[scn][oc][p]]
                y = [y0[scn]+0.25+dy, y0[scn]+0.75+dy]
                traces.append(
                    {'x': x, 'y': y, 'mode': 'lines', 'line': {'color': base_col[scn], 'width': 2}, 'text': p + '% probability', 'hoverinfo': 'x+text'}
                )
            x = [data[scn][oc]['17'], data[scn][oc]['83']]
            y = [y0[scn]+0.5+dy, y0[scn]+0.5+dy]
            traces.append(
                {'x': x, 'y': y, 'mode': 'lines', 'line': {'color': base_col[scn], 'width': 2}, 'hoverinfo': 'none'}
            )
            traces.append(
                {'x': [data[scn][oc]['50']], 'y': [y0[scn]+0.5+dy], 'mode': 'markers', 'marker': {'color': base_col[scn], 'size': 8}, 'text': '50% probability', 'hoverinfo': 'x+text'}
            )

    x = [10, 2, 2, 10]
    y = [4, 4, 0, 0]
    traces.append(
        {'x': x, 'y': y, 'fill': 'toself', 'fillcolor': '#d6d6d6', 'mode': 'none', 'xaxis': 'x2', 'yaxis': 'y2', 'hoverinfo': 'none'}
    )
    for p in [0, 4, 8, 12]:
        traces.append(
            {'x': [p, p], 'y': [1, 3], 'mode': 'lines', 'line': {'color': '#777777', 'width': 2}, 'xaxis': 'x2', 'yaxis': 'y2', 'hoverinfo': 'none'}
        )
    traces.append(
        {'x': [0, 4], 'y': [2, 2], 'mode': 'lines', 'line': {'color': '#777777', 'width': 2}, 'xaxis': 'x2', 'yaxis': 'y2', 'hoverinfo': 'none'}
    )
    traces.append(
        {'x': [8, 12], 'y': [2, 2], 'mode': 'lines', 'line': {'color': '#777777', 'width': 2}, 'xaxis': 'x2', 'yaxis': 'y2', 'hoverinfo': 'none'}
    )
    traces.append(
        {'x': [2, 10], 'y': [2, 2], 'mode': 'markers', 'marker': {'color': '#777777', 'size': 8}, 'xaxis': 'x2', 'yaxis': 'y2', 'hoverinfo': 'none'}
    )

    return traces

# ---------------------------------------------------------------------------

def decadal_traces(dtot, dmax, dscn):

    base_col = {'int_low': col[0], 'int': col[1], 'int_high': col[3], 'kopp': col[4]}

    pctl = list(dtot.keys())[1:-1]

    d0 = 0
    dx = 3.5

    traces = []

    for iy, yr in enumerate(dec_yrs):

        if np.floor(yr/10)%2 == 0:
            x = [np.floor(yr/10)*10, np.ceil(yr/10)*10, np.ceil(yr/10)*10, np.floor(yr/10)*10]
            y = [-1000, -1000, 1000, 1000]
            traces.append(
                {'x': x, 'y': y, 'fill': 'toself', 'fillcolor': '#f6f6f6', 'mode': 'none', 'xaxis': 'x2'}
            )

        # total
        x = [yr, yr-dx, yr-dx, yr]
        x = [x0+d0 for x0 in x]
        y = [dtot['83'][iy], dtot['83'][iy], dtot['17'][iy], dtot['17'][iy]]
        y = [y0/10 for y0 in y]
        traces.append(
            {'x': x, 'y': y, 'fill': 'toself', 'fillcolor': fill_color(base_col[dscn], 0.85), 'mode': 'none', 'xaxis': 'x2', 'yaxis': 'y2', 'text': 'Likely range [' + str(int(y[2])) + ', ' + str(int(y[0])) + ']', 'hovertemplate': "<b>%{text}</b><br><br>"}# +
            # "%{yaxis.title.text}: %{y:$,.0f}<br>" +
            # "%{xaxis.title.text}: %{x:.0%}<br>" +
            # "Number Employed: %{marker.size:,}" +
            # "<extra></extra>"}
        )
        x = [yr, yr-dx]
        x = [x0+d0 for x0 in x]
        y = [dtot['50'][iy], dtot['50'][iy]]
        y = [y0/10 for y0 in y]
        traces.append(
            {'x': x, 'y': y, 'mode': 'lines', 'line': {'color': '#000000', 'width': 3}, 'xaxis': 'x2', 'yaxis': 'y2', 'text': 'Most likely (median)', 'hoverinfo': 'y+text'}
        )

        # max
        x = [yr, yr+dx, yr+dx, yr]
        x = [x0+d0 for x0 in x]
        y = [dmax['83'][iy], dmax['83'][iy], dmax['17'][iy], dmax['17'][iy]]
        traces.append(
            {'x': x, 'y': y, 'fill': 'toself', 'fillcolor': fill_color(base_col[dscn], 0.25), 'mode': 'none', 'xaxis': 'x2', 'yaxis': 'y2', 'text': 'Likely range [' + str(int(y[2])) + ', ' + str(int(y[0])) + ']', 'hoverinfo': 'text'}
        )
        x = [yr, yr+dx]
        x = [x0+d0 for x0 in x]
        y = [dmax['50'][iy], dmax['50'][iy]]
        traces.append(
            {'x': x, 'y': y, 'mode': 'lines', 'line': {'color': '#000000', 'width': 3}, 'xaxis': 'x2', 'yaxis': 'y2', 'text': 'Most likely (median)', 'hoverinfo': 'y+text'}
        )

    # legend
    traces.extend([
        {'x': [-1, 0, 0, -1], 'y': [2, 2, -2, -2], 'fill': 'toself', 'fillcolor': fill_color(base_col[dscn], 0.85), 'mode': 'none', 'xaxis': 'x3', 'yaxis': 'y3', 'hoverinfo': 'none'},
        {'x': [-1, 0], 'y': [0, 0], 'mode': 'lines', 'line': {'color': '#000000', 'width': 3}, 'xaxis': 'x3', 'yaxis': 'y3', 'hoverinfo': 'none'},
        {'x': [0, 1, 1, 0], 'y': [5, 5, 1, 1], 'fill': 'toself', 'fillcolor': fill_color(base_col[dscn], 0.25), 'mode': 'none', 'xaxis': 'x3', 'yaxis': 'y3', 'hoverinfo': 'none'},
        {'x': [0, 1], 'y': [3, 3], 'mode': 'lines', 'line': {'color': '#000000', 'width': 3}, 'xaxis': 'x3', 'yaxis': 'y3', 'hoverinfo': 'none'}
    ])

    return traces

# ---------------------------------------------------------------------------

modebar_config = {
    'modeBarButtonsToRemove': ['toggleSpikelines', 'sendDataToCloud', 'hoverClosestCartesian', 'hoverCompareCartesian'],
    'displaylogo': False
}

prjn_layout = {
    # 'title': 'Projections of exceedance days per year',
    'yaxis': {
        'title': 'Flooding days per year',
        'automargin': True,
        'range': [0, 370]
    },
    'xaxis': {
        'title': 'Year',
        'range': [2010, 2100],
    },
    'margin': {'t': 25},
    'hovermode': 'x'
}

noaa_annotations = {
    'annotations': [
        {
            'xref': 'paper',
            'yref': 'paper',
            'x': 1.077,
            'y': 0.82,
            'text': 'Medians and likely',
            'font': {'size': 12},
            'xanchor': 'left',
            'showarrow': False
        },
        {
            'xref': 'paper',
            'yref': 'paper',
            'x': 1.077,
            'y': 0.77,
            'text': 'ranges (17-83%)',
            'font': {'size': 12},
            'xanchor': 'left',
            'showarrow': False
        }
    ]
}

legx0 = 0.85
decadal_layout = {
    'margin': {'t': 25},
    'showlegend': False,
    'hovermode': 'x',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'yaxis': {
        'showgrid': False,
        'zeroline': False,
        'ticks': [],
        'showticklabels': False,
        'range': [0, 500]
    },
    'xaxis': {
        'domain': [0., legx0],
        'showgrid': False,
        'zeroline': False,
        'ticks': [],
        'showticklabels': False,
        'range': [2020, 2060],
    },
    'yaxis2': {
        'anchor': 'y2',
        'title': 'Flooding days per year',
        'automargin': True,
        'layer': 'above traces',
    },
    'xaxis2': {
        'anchor': 'x2',
        'domain': [0., legx0],
        'title': 'Year',
        'range': [2020, 2060],
        'showgrid': False,
        'tickvals': dec_yrs,
        'ticktext': [str(int(np.floor(y/10)*10)) + 's' for y in dec_yrs],
    },
    'yaxis3': {
        'anchor': 'y3',
        'showgrid': False,
        'zeroline': False,
        'ticks': [],
        'showticklabels': False,
        'range': [-15, 8],
        'fixedrange': True,
        'automargin': True,
    },
    'xaxis3': {
        'anchor': 'x3',
        'domain': [legx0, 1.0],
        'showgrid': False,
        'zeroline': False,
        'ticks': [],
        'showticklabels': False,
        'range': [-2, 2],
        'fixedrange': True
    },
    'annotations': [
        {
            'xref': 'x3',
            'yref': 'y3',
            'x': -1.5,
            'y': 7.,
            'text': 'Medians and likely',
            'font': {'size': 12},
            'xanchor': 'left',
            'showarrow': False
        },
        {
            'xref': 'x3',
            'yref': 'y3',
            'x': -1.5,
            'y': 6.,
            'text': 'ranges (17-83%)',
            'font': {'size': 12},
            'xanchor': 'left',
            'showarrow': False
        },
        {
            'xref': 'x3',
            'yref': 'y3',
            'x': -0.5,
            'y': -2.75,
            'textangle': 270,
            'text': 'Average year in each decade',
            'font': {'size': 12},
            'yanchor': 'top',
            'showarrow': False
        },
        {
            'xref': 'x3',
            'yref': 'y3',
            'x': 0.5,
            'y': 0.25,
            'textangle': 270,
            'text': 'Maximum year in each decade',
            'font': {'size': 12},
            'yanchor': 'top',
            'showarrow': False
        }
    ]
}

analysis_layout = {
    'height': 300,
    'margin': {'t': 25, 'r': 10},
    'showlegend': False,
    'hovermode': 'x',
    'yaxis': {
        'range': [1.25, 5.75],
        'tickvals': [2, 3, 4, 5],
        'ticktext': ['Kopp et al. (2014) RCP8.5', 'NOAA Intermediate Low', 'NOAA Intermediate', 'NOAA Intermediate High'],
        'automargin': True,
        'zeroline': False,
        'fixedrange': True,
    },
    'xaxis': {
        'domain': [0.0, 0.72],
        'title': 'Year',
        'range': [2010, 2100],
        'zeroline': False,
    },
    'yaxis2': {
        'domain': [0.6, 0.95],
        'anchor': 'y2',
        'showgrid': False,
        'zeroline': False,
        'ticks': [],
        'showticklabels': False,
        'fixedrange': True,
    },
    'xaxis2': {
        'domain': [0.77, 1.0],
        'anchor': 'x2',
        'showgrid': False,
        'zeroline': False,
        'ticks': [],
        'showticklabels': False,
        'fixedrange': True,
    },
}

firstyear_layout = {
    'annotations': [
        {
            'xref': 'x2',
            'yref': 'y2',
            'x': j,
            'y': 0,
            'text': str(k),
            'font': {'size': 12},
            'showarrow': False
        } for j, k in enumerate([5, 17, 50, 83, 95])
    ] + [
        {
            'xref': 'x2',
            'yref': 'y2',
            'x': 2,
            'y': -3,
            'text': '% probability',
            'font': {'size': 12},
            'showarrow': False
        }
    ],
}

occ2chrnc_layout = {
    'yaxis2': {
        'domain': [0.5, 0.95],
        'anchor': 'y2',
        'showgrid': False,
        # 'zeroline': False,
        'ticks': [],
        'showticklabels': False,
        'fixedrange': True,
    },
    'annotations': [
        {
            'xref': 'x2',
            'yref': 'y2',
            'x': j,
            'y': -1,
            'text': str(k),
            'font': {'size': 12},
            'showarrow': False
        } for j, k in zip([0, 2, 4, 8, 10, 12],[17, 50, 83, 17, 50, 83])
    ] + [
        {
            'xref': 'x2',
            'yref': 'y2',
            'x': 6,
            'y': -3.25,
            'text': '% probability',
            'font': {'size': 12},
            'showarrow': False
        },
        {
            'xref': 'x2',
            'yref': 'y2',
            'x': 2,
            'y': 5.25,
            'text': 'occasional',
            'font': {'size': 12},
            'showarrow': False
        },
        {
            'xref': 'x2',
            'yref': 'y2',
            'x': 10,
            'y': 5.25,
            'text': 'chronic',
            'font': {'size': 12},
            'showarrow': False,
        }
    ],
}

# ---------------------------------------------------------------------------

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)#, external_stylesheets=external_stylesheets)
app.title = 'Flooding Days'

app.layout = html.Div(id='main-div', children=[

    # -----------------------------------------------------------------------
    # page header

    html.Div(id='page-header', children=[

        html.Img(className='page-header-logo',
            src='./assets/nasaLogo.png',
            style={'float': 'left', 'height': '50px', 'margin-top': '10px'}
        ),

        html.H3(children='FLOODING DAYS',
            style={
                'float': 'left',
                'color': '#1f77b4',
                'font-weight': 'bold'
            }
        ),
        html.H3(children='Projection Tool',
            style={
                'float': 'left',
                'margin-left': '9px',
                'color': '#777777',
                'font-weight': 'bold'
            }
        ),
        html.H3(children='[ prototype ]',
            style={
                'float': 'left',
                'margin-left': '9px',
                'color': '#777777',
                'font-size': '18px',
                # 'font-weight': 'bold'
            }
        ),

        html.Div(style={'float': 'right', 'margin-top': '5px'}, children=[
            html.Div('Developed by:', style={'font-size': '12px', 'color': '#777777'}),
            html.A(href='http://uhslc.soest.hawaii.edu', target='_blank',
                children=[
                    html.Img(
                        src='./assets/uhslcLogo.png',
                        style={'height': '30px'}
                    ),
                ]
            ),
        ]),

        html.Div(style={'clear': 'both'}),

    ]),

    # -----------------------------------------------------------------------
    # app

    html.Div(id='app-container', children=[

        # -------------------------------------------------------------------
        # location and threshold

        html.Div(id='app-header', children=[

            html.Div(style={'float': 'left', 'width': '32%', 'margin-top': '0px', 'margin-left': '1%', 'margin-right': '2%'}, children=[

                html.Div(style={'position': 'relative'}, children=[
                    html.Div('Location',
                        style={'display': 'inline-block', 'margin': '0px 0px 2px 2px', 'color': '#1f77b4', 'font-size': '20px', 'font-weight': 'bold'}
                    ),
                    html.Div(
                        className = 'help help-left',
                        style = {'display': 'inline-block', 'margin': '0px 0px 2px 4px', 'color': '#999999', 'font-size': '20px'},
                        children = [
                            dcc.Markdown('''
This **dropdown selector** contains >90 coastal locations from around the United States and its island territories for which there is sufficient tide gauge data to make robust projections of future flood frequency.

**Search** for locations or state abbreviations (e.g., NC, CA, etc.) by typing in the text box.
                            '''),
                            '\u003f\u20dd'
                        ]
                    ),
                ]),

                dcc.Dropdown(
                    id = 'station-picker',
                    options = station_list,
                    value = uid_init,
                    searchable = True,
                    clearable = False,
                    style = {'height': '40px', 'display': 'block', 'margin-right': '30px'}
                ),
            ]),

            html.Div(style={'float': 'left', 'width': '62%', 'margin-right': '1%'}, children=[

                html.Div(style={'display': 'flex', 'justify-content': 'space-between', 'position': 'relative'}, children=[

                    html.Div('Flooding Threshold',
                        style={'display': 'inline-block', 'margin': '0px 0px 7px -2px', 'color': '#1f77b4', 'font-size': '20px', 'font-weight': 'bold'}
                    ),

                    html.Div(children=[
                        html.Div(str(int(slider_thrsh_init)),
                            id='threshold-slider-value',
                            style={'display': 'inline-block', 'margin': '0px 0px 7px -2px', 'color': '#1f77b4', 'font-size': '20px', 'font-weight': 'bold'}
                        ),

                        html.Div('cm above MHHW',
                            style={'display': 'inline-block', 'margin': '0px 0px 7px 4px', 'color': '#777777', 'font-size': '16px', 'font-weight': 'normal'}
                        ),

                        html.Div(
                            className = 'help help-right',
                            style = {'display': 'inline-block', 'margin': '0px 0px 2px 4px', 'color': '#999999', 'font-size': '20px'},
                            children = [
                                dcc.Markdown('''
**MHHW** stands for *Mean Higher High Water*, which is defined as the average highest observed water level per tidal day experienced at this location during the period 1983-2001. This 19-year period is defined as the current National Tidal Datum Epoch (NTDE). More information [**here**](https://tidesandcurrents.noaa.gov/datum_options.html).
                                '''),
                                '\u003f\u20dd'
                            ]
                        ),
                    ]),
                ]),

                html.Div(
                    children=[
                        dcc.Slider(
                            id = 'threshold-slider',
                            min = min(thresholds),
                            max = max(thresholds),
                            value = int(slider_thrsh_init),
                            marks = {str(t): str(t) for t in thresholds if t % 10 == 0},
                            updatemode = 'drag'
                            # vertical = True,
                        )],
                    style = {'display': 'block', 'width': ''},
                ),

                html.Div(children=[
                    html.Div(style={'display': 'inline-block', 'margin': '40px 0px 0px -2px', 'color': '#777777', 'font-size': '14px', 'vertical-align': 'top'}, children=[

                        html.Div(style={'position': 'relative'}, children=[
                            html.Div('NOAA flooding thresholds for',
                                style={'display': 'inline-block', 'font-weight': 'bold'}
                            ),
                            html.Div(stations[uid_init]['name'],
                                id='noaa-thrsh-station',
                                style={'display': 'inline-block', 'margin-left': '4px', 'color': '#1f77b4', 'font-size': '14px', 'font-weight': 'bold'}
                            ),
                            html.Div(':',
                                style={'display': 'inline-block', 'margin-left': '1px', 'font-weight': 'bold'}
                            ),
                            html.Div(
                                className = 'help help-right',
                                style = {'display': 'inline-block', 'margin': '0px 0px 2px 4px', 'color': '#999999', 'font-size': '16px'},
                                children = [
                                    dcc.Markdown('''
**NOAA flooding thresholds** are based on a statistical relationship between vulnerability and mean tidal range. Details of this analysis can be found in the following report:

Sweet, W. V., Dusek, G., Obeysekera, J., & Marra, J. J. (2018). NOAA Technical Report NOS CO-OPS 086: Patterns And Projections Of High Tide Flooding Along The U.S. Coastline Using A Common Impact Threshold. *Silver Spring, Maryland*.

Download a .pdf of the report [**here**](https://tidesandcurrents.noaa.gov/publications/techrpt86_PaP_of_HTFlooding.pdf).
                                    '''),
                                    '\u003f\u20dd'
                                ]
                            ),
                        ]),

                        html.Div(children=[
                            html.Div('Minor:',
                                style={'display': 'inline-block', 'color': '#777777', 'font-size': '14px', 'font-weight': 'bold'}
                            ),
                            html.Div(str(int(noaa_thrsh_init['minor'])),
                                id='noaa-thrsh-minor',
                                style={'display': 'inline-block', 'margin': '0px 0px 0px 4px', 'color': '#1f77b4', 'font-size': '14px', 'font-weight': 'bold'}
                            ),
                            html.Div('cm above MHHW',
                                style={'display': 'inline-block', 'margin': '0px 0px 0px 4px', 'color': '#777777', 'font-size': '14px', 'font-weight': 'normal'}
                            ),
                            html.Div('Moderate:',
                                style={'display': 'inline-block', 'margin': '0px 0px 0px 20px', 'color': '#777777', 'font-size': '14px', 'font-weight': 'bold'}
                            ),
                            html.Div(str(int(noaa_thrsh_init['moderate'])),
                                id='noaa-thrsh-moderate',
                                style={'display': 'inline-block', 'margin-left': '4px', 'color': '#1f77b4', 'font-weight': 'bold'}
                            ),
                            html.Div('cm above MHHW',
                                style={'display': 'inline-block', 'margin-left': '4px'}
                            ),
                        ]),

                    ]),
                ]),

            ]),

            html.Div(style={'clear': 'both'}),
        ]),

        # -------------------------------------------------------------------
        # tabs

        dcc.Tabs(id='tabs-container', value='ann_prjn', children=[

            dcc.Tab(label='Annual projections', value='ann_prjn', className='custom-tab', selected_className='custom-tab-selected', children=[

                html.Div(id='projections-header', children=[
                    dcc.Markdown('###### Flooding days during the 21st century', className='section-title'),
                    html.Div('The following figure shows the number of days per year that sea level in ', className='header-text'),
                    html.Div(stations[uid_init]['name'], id='annual-header-station', className='header-text', style={'color': col[0], 'font-weight': 'bold'}),
                    html.Div('will exceed ', className='header-text'),
                    html.Div(str(int(slider_thrsh_init)) + ' cm', id='annual-header-threshold', className='header-text', style={'color': col[0], 'font-weight': 'bold'}),
                    html.Div('above MHHW.', className='header-text'),
                    html.Div(style={'clear': 'both', 'margin-bottom': '20px'}),
                ]),

                html.Div('Based on local mean sea level projection:', className='header-text', style={'vertical-align': 'top'}),
                dcc.Dropdown(
                    id = 'projection-picker',
                    options = [
                        {'label': 'NOAA Sea Level Rise Scenarios', 'value': 'noaa'},
                        {'label': 'Kopp et al. (2014) RCP8.5', 'value': 'kopp'},
                    ],
                    value = 'noaa',
                    searchable = False,
                    clearable = False,
                    style = {'height': '37px', 'width': '300px', 'display': 'inline-block', 'margin': '-5px 5px 0px 0px'}
                ),

                # html.Div(style={'display': 'inline-block'}, children=[
                #     dcc.RadioItems(
                #         id = 'projection-picker',
                #         options = [
                #             {'label': 'NOAA Sea Level Rise Scenarios', 'value': 'noaa'},
                #             {'label': 'Kopp et al. (2014) RCP8.5', 'value': 'kopp'},
                #         ],
                #         value = 'noaa',
                #         labelStyle = {'display': 'inline-block', 'margin-left': '15px'}
                #     ),
                # ]),

                dcc.Graph(
                    id = 'projections-fig',
                    figure = {
                        'data': noaa_traces(prjn_init),
                        'layout': prjn_layout,
                    },
                    config = modebar_config
                ),

            ]),

            dcc.Tab(label='Decadal projections', value='dec_prjn', className='custom-tab', selected_className='custom-tab-selected', children=[

                html.Div(id='decadal-header', children=[
                    dcc.Markdown('###### Projections of flooding days by decade', className='section-title'),
                    html.Div('The figure below shows the average and maximum number of days per year in future decades that sea level in ', className='header-text'),
                    html.Div(stations[uid_init]['name'], id='decadal-header-station', className='header-text', style={'color': col[0], 'font-weight': 'bold'}),
                    html.Div('will exceed ', className='header-text'),
                    html.Div(str(int(slider_thrsh_init)) + ' cm', id='decadal-header-threshold', className='header-text', style={'color': col[0], 'font-weight': 'bold'}),
                    html.Div('above MHHW. The total number of events per decade is the average multiplied by ten.', className='header-text'),
                    html.Div(style={'clear': 'both', 'margin-bottom': '20px'}),
                ]),

                html.Div('Based on local mean sea level projection:', className='header-text', style={'vertical-align': 'top'}),
                dcc.Dropdown(
                    id = 'decadal-lmslr-picker',
                    options = dec_lmslr_drpdwn,
                    value = dec_lmslr_init,
                    searchable = False,
                    clearable = False,
                    style = {'height': '37px', 'width': '300px', 'display': 'inline-block', 'margin': '-5px 5px 0px 0px'}
                ),

                dcc.Graph(
                    id = 'decadal-fig',
                    figure = {
                        'data': decadal_traces(dtot_init, dmax_init, dec_lmslr_init),
                        'layout': decadal_layout,
                    },
                    config = modebar_config
                ),

            ]),

            dcc.Tab(label='Analysis', value='analysis', className='custom-tab', selected_className='custom-tab-selected', children=[

                html.Div(id='firstyear-header', children=[
                    dcc.Markdown('###### Question \#1', className='section-title'),
                    html.Div('What year will ', className='header-text'),
                    html.Div(stations[uid_init]['name'], id='firstyear-header-station', className='header-text', style={'color': col[0], 'font-weight': 'bold'}),
                    html.Div('first experience', className='header-text'),
                    dcc.Dropdown(
                        id = 'numxd-picker',
                        options = fyr_cnts_drpdwn,
                        value = fyrc_init,
                        searchable = False,
                        clearable = False,
                        style = {'height': '37px', 'width': '50px', 'display': 'inline-block', 'margin': '-5px 5px 0px 0px'}
                    ),
                    html.Div('days with sea level exceeding', className='header-text'),
                    html.Div(str(int(slider_thrsh_init)) + ' cm', id='firstyear-header-threshold', className='header-text', style={'color': col[0], 'font-weight': 'bold'}),
                    html.Div('above MHHW?', className='header-text')
                ]),

                dcc.Graph(
                    id = 'firstyear-fig',
                    figure = {
                        'data': firstyear_traces(fyrs_init, fyrc_init),
                        'layout': firstyear_layout,
                    },
                    config = modebar_config
                ),

                html.Div(id='occ2chrnc-header', children=[
                    dcc.Markdown('###### Question \#2', className='section-title'),
                    # html.Div('For ', className='header-text'),
                    # html.Div(stations[uid_init]['name'], id='occ2chrnc-header-station', className='header-text', style={'color': col[0], 'font-weight': 'bold'}),
                    html.Div('When will the frequency of exceedances above the', className='header-text'),
                    html.Div(str(int(slider_thrsh_init)) + ' cm', id='occ2chrnc-header-threshold', className='header-text', style={'color': col[0], 'font-weight': 'bold'}),
                    html.Div('threshold transition from occasional to chronic?', className='header-text')
                ]),

                dcc.Graph(
                    id = 'occ2chrnc-fig',
                    figure = {
                        'data': occ2chrnc_traces(o2c_init),
                        'layout': occ2chrnc_layout,
                    },
                    config = modebar_config
                ),

            ]),

        ], colors={
            'border': '#d6d6d6',
            'primary': '#d6d6d6',
            'background': '#efefef'
        }),
    ]),
])

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# CALLBACKS

# ---------------------------------------------------------------------------
# header

@app.callback(
    dash.dependencies.Output('threshold-slider-value', 'children'),
    [dash.dependencies.Input('threshold-slider', 'value')]
    )
def update_threshold_slider_value(selected_threshold):
    return str(selected_threshold)

@app.callback(
    dash.dependencies.Output('threshold-slider', 'value'),
    [dash.dependencies.Input('station-picker', 'value')]
    )
def update_threshold_slider_value(selected_station):

    fname = './json/' + selected_station + '/' \
        + 'thresholds.json'
    with open(fname, 'r') as f:
        noaa_thrsh = json.load(f)

    return int(noaa_thrsh['minor'])

@app.callback(
    dash.dependencies.Output('noaa-thrsh-station', 'children'),
    [dash.dependencies.Input('station-picker', 'value')]
    )
def update_annual_projections_location_text(selected_station):
    return str(stations[selected_station]['name'])

@app.callback(
    dash.dependencies.Output('noaa-thrsh-moderate', 'children'),
    [dash.dependencies.Input('station-picker', 'value')]
    )
def update_moderate_threshold(selected_station):

    fname = './json/' + selected_station + '/' \
        + 'thresholds.json'
    with open(fname, 'r') as f:
        noaa_thrsh = json.load(f)

    return str(int(noaa_thrsh['moderate']))

@app.callback(
    dash.dependencies.Output('noaa-thrsh-minor', 'children'),
    [dash.dependencies.Input('station-picker', 'value')]
    )
def update_minor_threshold(selected_station):

    fname = './json/' + selected_station + '/' \
        + 'thresholds.json'
    with open(fname, 'r') as f:
        noaa_thrsh = json.load(f)

    return str(int(noaa_thrsh['minor']))

# ---------------------------------------------------------------------------
# annual projections

@app.callback(
    dash.dependencies.Output('annual-header-threshold', 'children'),
    [dash.dependencies.Input('threshold-slider', 'value')]
    )
def update_annual_projections_threshold_text(selected_threshold):
    return str(selected_threshold) + ' cm'

@app.callback(
    dash.dependencies.Output('annual-header-station', 'children'),
    [dash.dependencies.Input('station-picker', 'value')]
    )
def update_annual_projections_location_text(selected_station):
    return str(stations[selected_station]['name'])

@app.callback(
    dash.dependencies.Output('projections-fig', 'figure'),
    [dash.dependencies.Input('station-picker', 'value'), dash.dependencies.Input('threshold-slider', 'value'), dash.dependencies.Input('projection-picker', 'value')]
    )
def update_projection(selected_station, selected_threshold, selected_projection):

    fname = './json/' + selected_station + '/' \
        + '{:0>3}'.format(selected_threshold) + '/' + 'projections.json'
    with open(fname, 'r') as f:
        data = json.load(f)

    if selected_projection == 'noaa':
        return {
            'data': noaa_traces(data),
            'layout': {**prjn_layout, **noaa_annotations}
        }
    elif selected_projection == 'kopp':
        return {
            'data': kopp_traces(data),
            'layout': prjn_layout
        }

# ---------------------------------------------------------------------------
# decadal projections

@app.callback(
    dash.dependencies.Output('decadal-header-threshold', 'children'),
    [dash.dependencies.Input('threshold-slider', 'value')]
    )
def update_annual_projections_threshold_text(selected_threshold):
    return str(selected_threshold) + ' cm'

@app.callback(
    dash.dependencies.Output('decadal-header-station', 'children'),
    [dash.dependencies.Input('station-picker', 'value')]
    )
def update_annual_projections_location_text(selected_station):
    return str(stations[selected_station]['name'])

@app.callback(
    dash.dependencies.Output('decadal-fig', 'figure'),
    [dash.dependencies.Input('station-picker', 'value'), dash.dependencies.Input('threshold-slider', 'value'), dash.dependencies.Input('decadal-lmslr-picker', 'value')]
    )
def update_projection(selected_station, selected_threshold, selected_projection):

    fname = './json/' + selected_station + '/' \
        + '{:0>3}'.format(selected_threshold) + '/' + 'dec_total.json'
    with open(fname, 'r') as f:
        dtot = json.load(f)

    fname = './json/' + selected_station + '/' \
        + '{:0>3}'.format(selected_threshold) + '/' + 'dec_max.json'
    with open(fname, 'r') as f:
        dmax = json.load(f)

    return {
        'data': decadal_traces(dtot[selected_projection], dmax[selected_projection], selected_projection),
        'layout': decadal_layout
    }

# ---------------------------------------------------------------------------
# first year figure

@app.callback(
    dash.dependencies.Output('firstyear-fig', 'figure'),
    [dash.dependencies.Input('station-picker', 'value'),
    dash.dependencies.Input('threshold-slider', 'value'),
    dash.dependencies.Input('numxd-picker', 'value')]
    )
def update_firstyear(selected_station, selected_threshold, selected_count):

    fname = './json/' + selected_station + '/' \
        + '{:0>3}'.format(selected_threshold) + '/' + 'first_years.json'
    with open(fname, 'r') as f:
        data = json.load(f)

    return {
        'data': firstyear_traces(data, str(selected_count)),
        'layout': {**analysis_layout, **firstyear_layout}
    }

@app.callback(
    dash.dependencies.Output('firstyear-header-threshold', 'children'),
    [dash.dependencies.Input('threshold-slider', 'value')]
    )
def update_firstyear_header_threshold(selected_threshold):
    return str(selected_threshold) + ' cm'

@app.callback(
    dash.dependencies.Output('firstyear-header-station', 'children'),
    [dash.dependencies.Input('station-picker', 'value')]
    )
def update_firstyear_header_threshold(selected_station):
    return str(stations[selected_station]['name'])

# ---------------------------------------------------------------------------
# occasional to chronic figure

@app.callback(
    dash.dependencies.Output('occ2chrnc-fig', 'figure'),
    [dash.dependencies.Input('station-picker', 'value'),
    dash.dependencies.Input('threshold-slider', 'value')]
    )
def update_occ2chrnc(selected_station, selected_threshold):

    fname = './json/' + selected_station + '/' \
        + '{:0>3}'.format(selected_threshold) + '/' + 'occ_to_chrnc.json'
    with open(fname, 'r') as f:
        data = json.load(f)

    return {
        'data': occ2chrnc_traces(data),
        'layout': {**analysis_layout, **occ2chrnc_layout}
    }

@app.callback(
    dash.dependencies.Output('occ2chrnc-header-threshold', 'children'),
    [dash.dependencies.Input('threshold-slider', 'value')]
    )
def update_occ2chrnc_header_threshold(selected_threshold):
    return str(selected_threshold) + ' cm'

# @app.callback(
#     dash.dependencies.Output('occ2chrnc-header-station', 'children'),
#     [dash.dependencies.Input('station-picker', 'value')]
#     )
# def update_occ2chrnc_header_threshold(selected_station):
#     return str(stations[selected_station]['name'])

# ---------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)

# ---------------------------------------------------------------------------
