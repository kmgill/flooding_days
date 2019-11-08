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
uid_init = '1612340'

fname = './json/' + uid_init + '/' + 'thresholds.json'
with open(fname, 'r') as f:
    noaa_thrsh_init = json.load(f)
slider_thrsh_init = '{:0>3}'.format(int(noaa_thrsh_init['minor']))

slider_marks_base = {t: {'label': str(t)} for t in thresholds if t % 10 == 0}
slider_marks_noaa = {
    int(noaa_thrsh_init['minor']):
        {'label': '\u25B2\nMinor',
            'style': {'color': col[1], 'white-space': 'pre-line'}},
    int(noaa_thrsh_init['moderate']):
        {'label': '\u25B2\nModerate',
            'style': {'color': col[3], 'white-space': 'pre-line'}},
}
slider_marks = {**slider_marks_base, **slider_marks_noaa}

# import sys; sys.exit()

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
    'displaylogo': False,
    # 'displayModeBar': True
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
        'title': 'Decade',
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

            html.Div(id='header-group-left', children=[

                html.Div(style={'position': 'relative'}, children=[
                    html.Div('Location',
                        className = 'header-title text-highlight',
                        style={'margin': '0px 0px 2px 2px'}
                    ),
                    html.Div(
                        className = 'help help-short help-left',
                        children = [
                            dcc.Markdown('''
**Choose** from >90 coastal locations from around the United States and its island territories. These are locations where there is sufficient tide gauge data to make robust projections of future flood frequency.

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
                    style = {'height': '37px', 'display': 'block', 'margin-right': '30px'}
                ),

                html.Div(
                    id = 'for-help',
                    children = [
                        html.Div('\u003f\u20dd',
                            id = 'for-help-qmark',
                        ),
                        html.Div(
                            id = 'for-help-buff',
                        ),
                        html.Div('For help and information, hover over the \u003f\u20dd symbols.',
                            id = 'for-help-text',
                        ),
                    ],
                ),

            ]),

            html.Div(id='header-group-right', children = [

                html.Div(style = {'display': 'flex', 'justify-content': 'space-between', 'position': 'relative'}, children=[

                    html.Div('Flooding Threshold',
                        className = 'header-title text-highlight',
                        style = {'margin': '0px 0px 7px -2px'}
                    ),

                    html.Div(children=[
                        html.Div(str(int(slider_thrsh_init)),
                            id = 'threshold-slider-value',
                            className = 'header-title text-highlight',
                            style = {'margin': '0px 0px 7px -2px'}
                        ),

                        html.Div('above MHHW',
                            className = 'header-text',
                            style = {'margin': '0px 0px 7px 6px', 'font-size': '16px'}
                        ),

                        html.Div(
                            className = 'help help-short help-right',
                            children = [
                                dcc.Markdown('''
**MHHW** stands for *Mean Higher High Water*, which is defined as the average of the highest observed water level at the selected location on each tidal day during the period 1983-2001.

This specific 19-year period, 1983–2001, is the current National Tidal Datum Epoch (NTDE).

More information [**here**](https://tidesandcurrents.noaa.gov/datum_options.html).
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
                            marks = slider_marks,
                            updatemode = 'drag'
                            # vertical = True,
                        )],
                    style = {'display': 'block', 'width': ''},
                ),

                html.Div(className='threshold-info', children=[
                    html.Div(
                        style = {'display': 'inline-block',
                            'margin-left': '-2px'},
                        children=[

                            html.Div(style={'position': 'relative'}, children=[
                                html.Div(className='min-mod-div', children=[
                                    html.Div('NOAA flooding thresholds for',
                                        className = 'header-text',
                                        style={'font-weight': 'bold', 'margin-right': '4px', 'vertical-align': 'top'}
                                    ),
                                ]),
                                html.Div(className='min-mod-div', children=[
                                    html.Div(stations[uid_init]['name'],
                                        id='noaa-thrsh-station',
                                        className = 'header-text text-highlight',
                                        style={'margin-right': '1px', 'vertical-align': 'top'}
                                    ),
                                    html.Div(':',
                                        className = 'header-text',
                                        style={'font-weight': 'bold', 'vertical-align': 'top'}
                                    ),
                                    html.Div(
                                        className = 'help help-short help-right',
                                        children = [
                                            dcc.Markdown('''
**NOAA flooding thresholds** are based on a statistical relationship between mean tidal range and vulnerability to high water levels.

Details of this analysis can be found in a NOAA report (Sweet et al., 2018), which can be accessed [**here**](https://tidesandcurrents.noaa.gov/publications/techrpt86_PaP_of_HTFlooding.pdf).
                                            '''),
                                            '\u003f\u20dd'
                                        ]
                                    ),
                                ]),
                            ]),
                            html.Div(children=[
                                html.Div(
                                    id = 'min-div',
                                    className = 'min-mod-div',
                                    children = [
                                        html.Div('Minor:',
                                            className = 'header-text',
                                            style={'font-weight': 'bold'}
                                        ),
                                        html.Div(str(int(noaa_thrsh_init['minor'])),
                                            id='noaa-thrsh-minor',
                                            className = 'header-text',
                                            style = {'margin': '0px 4px 0px 4px', 'color':
                                                col[1], 'font-weight': 'bold'}
                                        ),
                                        html.Div('above MHHW',
                                            className = 'header-text',
                                        ),
                                    ]
                                ),
                                html.Div(
                                    className='min-mod-div',
                                    children=[
                                        html.Div('Moderate:',
                                            className = 'header-text',
                                            style={'font-weight': 'bold'}
                                        ),
                                        html.Div(str(int(noaa_thrsh_init['moderate'])),
                                            id='noaa-thrsh-moderate',
                                            className = 'header-text',
                                            style = {'margin': '0px 4px 0px 4px', 'color':
                                                col[3], 'font-weight': 'bold'}
                                        ),
                                        html.Div('above MHHW',
                                            className = 'header-text',
                                        ),
                                    ]
                                ),
                            ]),
                        ]
                    ),

                    html.Div(
                        id = 'unit-switcher-div',
                        children=[

                            dcc.RadioItems(
                                id = 'unit-switcher',
                                className = 'header-text',
                                options = [
                                    {'label': 'Inches', 'value': 'in'},
                                    {'label': 'Centimeters', 'value': 'cm'},
                                ],
                                value = 'cm',
                                inputStyle={'margin-right': '10px', 'background-color': '#1f77b4'}
                            )

                        ]
                    ),
                ]),

            ]), # end threshold group

            html.Div(style={'clear': 'both'}),

        ]), # end control panel

        # -------------------------------------------------------------------
        # tabs

        dcc.Tabs(id='tabs-container', value='ann_prjn', children=[

            dcc.Tab(label='Annual projections', value='ann_prjn', className='custom-tab', selected_className='custom-tab-selected', children=[

                html.Div(id='projections-header', children=[
                    html.Div(style={'position': 'relative'}, children=[
                        dcc.Markdown('###### Flooding days during the 21st century', className='tab-title'),
#                     html.Div(
#                         className = 'help help-long help-left',
#                         children = [
#                             dcc.Markdown('''
# Placeholder
#                             '''),
#                             '\u003f\u20dd'
#                         ]
#                     ),
                    ]),
                    html.Div('The graph below shows the number of days per year that sea level in ', className='tab-text'),
                    html.Div(stations[uid_init]['name'], id='annual-header-station', className='tab-text text-highlight'),
                    html.Div('is projected to exceed ', className='tab-text'),
                    html.Div(str(int(slider_thrsh_init)) + ' cm', id='annual-header-threshold', className='tab-text text-highlight'),
                    html.Div('above MHHW.', className='tab-text'),
                    html.Details([
                        html.Summary(
                            className = 'read-more-top',
                            children = ['Read more']
                        ),
                        html.Div(
                            className = 'read-more-content',
                            children = [
                                dcc.Markdown('''
These projections are based on unique, location-specific relationships between annual mean sea level, the top 1% of astronomical tides in each year, and annual counts of threshold exceedances. See *Details of the methodology* at the bottom of the page for additional information.

An interesting and essential feature of these graphs is that the number of flooding days per year does not necessarily increase smoothly in time. In most cases, there are inflection points where the frequency of flooding days increases rapidly, which may be useful when establishing planning horizons. In many locations around the United States and its territories, there are sharp inflection points around the mid-2030s that are related to the interaction between accelerating sea level rise due to climate change and a long-term, 18.6-year cycle in the amplitude of astronomical tides. For clear examples of this effect, check out the flooding days projections for Honolulu, HI, Friday Harbor, WA, and St. Petersburg, FL.
                                ''')
                            ]
                        )
                    ]),
                    html.Div(style={'clear': 'both', 'margin-bottom': '10px'}),
                ]),

                html.Div(style = {'position': 'relative'}, children=[
                    html.Div('Choose the local mean sea level projection(s) to use:', className='tab-text', style={'vertical-align': 'middle'}),
                    dcc.Dropdown(
                        id = 'projection-picker',
                        options = [
                            {'label': 'NOAA Sea Level Rise Scenarios', 'value': 'noaa'},
                            {'label': 'Kopp et al. (2014) RCP8.5', 'value': 'kopp'},
                        ],
                        value = 'noaa',
                        searchable = False,
                        clearable = False,
                        style = {'height': '35px', 'width': '300px', 'display': 'inline-block', 'margin': '-5px 5px 0px 0px'}
                    ),
                    html.Div(
                        className = 'help help-short help-right',
                        children = [
                            dcc.Markdown('''
The options provided here are **localized** mean sea level projections, which account for local and regional processes, such as *subsidence* (see [**here**](https://sealevel.nasa.gov/understanding-sea-level/regional-sea-level/subsidence)) and *ice melt fingerprints* (see [**here**](https://sealevel.nasa.gov/understanding-sea-level/regional-sea-level/ice-mass-loss)), that cause local sea level rise to differ from global average rise.

---

See *About local mean sea level projections* at the bottom of the page for more information about these options.
                            '''),
                            '\u003f\u20dd'
                        ]
                    ),
                ]),

                html.Div(style = {'position': 'relative'}, children = [
                    html.Div(
                        className = 'help help-graph help-short help-left',
                        style = {'zIndex': '100'},
                        children = [
                            dcc.Markdown('''
**Click-and-drag** on the graph to zoom.

**Hover** over the graph, and more options will appear above the legend, inlcuding the ability to save an image.
                            '''),
                            '\u003f\u20dd'
                        ]
                    ),
                    dcc.Graph(
                        id = 'projections-fig',
                        figure = {
                            'data': noaa_traces(prjn_init),
                            'layout': prjn_layout,
                        },
                        config = modebar_config
                    ),
                ]),

            ]),

            dcc.Tab(label='Decadal projections', value='dec_prjn', className='custom-tab', selected_className='custom-tab-selected', children=[

                html.Div(id='decadal-header', children=[
                    html.Div(style={'position': 'relative'}, children=[
                        dcc.Markdown('###### Projections of flooding days by decade', className='tab-title'),
#                     html.Div(
#                         className = 'help help-long help-left',
#                         children = [
#                             dcc.Markdown('''
# Placeholder
#                             '''),
#                             '\u003f\u20dd'
#                         ]
#                     ),
                    ]),
                    html.Div('The graph below shows the average and maximum number of days per year in future decades that sea level in ', className='tab-text'),
                    html.Div(stations[uid_init]['name'], id='decadal-header-station', className='tab-text', style={'color': col[0], 'font-weight': 'bold'}),
                    html.Div('will exceed ', className='tab-text'),
                    html.Div(str(int(slider_thrsh_init)) + ' cm', id='decadal-header-threshold', className='tab-text', style={'color': col[0], 'font-weight': 'bold'}),
                    html.Div('above MHHW. The total number of events per decade can be calculated by multiplying the average by ten.', className='tab-text'),
                    html.Details([
                        html.Summary(
                            className = 'read-more-top',
                            children = ['Read more']
                        ),
                        html.Div(
                            className = 'read-more-content',
                            children = [
                                dcc.Markdown('''
There is a tendency for threshold exceedances in sea level to cluster together in a small number of severe years rather than being evenly distributed in time (e.g., [Thompson et al., 2019](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2018JC014741)). Thus, planning for the *typical* or *average* year can substantially underestimate the number of events experienced in the occasional&mdash;*yet inevetible*&mdash;severe year. Depending on the combination of location, threshold, and decade of interest, the worst year of a decade my experience up to five times as many flooding days as the average year!
                                ''')
                            ]
                        )                    ]),
                    html.Div(style={'clear': 'both', 'margin-bottom': '10px'}),
                ]),

                html.Div(style = {'position': 'relative'}, children=[
                    html.Div('Based on local mean sea level projection:', className='tab-text', style={'vertical-align': 'middle'}),
                    dcc.Dropdown(
                        id = 'decadal-lmslr-picker',
                        options = dec_lmslr_drpdwn,
                        value = dec_lmslr_init,
                        searchable = False,
                        clearable = False,
                        style = {'height': '37px', 'width': '300px', 'display': 'inline-block', 'margin': '-5px 5px 0px 0px'}
                    ),
                    html.Div(
                        className = 'help help-short help-right',
                        children = [
                            dcc.Markdown('''
The options provided here are **localized** mean sea level projections, which account for local and regional processes, such as *subsidence* (see [**here**](https://sealevel.nasa.gov/understanding-sea-level/regional-sea-level/subsidence)) and *ice melt fingerprints* (see [**here**](https://sealevel.nasa.gov/understanding-sea-level/regional-sea-level/ice-mass-loss)), that cause local sea level rise to differ from global average rise.

---

See *About local mean sea level projections* at the bottom of the page for more information.
                            '''),
                            '\u003f\u20dd'
                        ]
                    ),
                ]),

                html.Div(style = {'position': 'relative'}, children = [
                    html.Div(
                        className = 'help help-graph help-short help-left',
                        style = {'zIndex': '100'},
                        children = [
                            dcc.Markdown('''
**Click-and-drag** on the graph to zoom.

**Hover** over the graph, and more options will appear above the legend, inlcuding the ability to save an image.
                            '''),
                            '\u003f\u20dd'
                        ]
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
            ]),

            dcc.Tab(label='Analysis', value='analysis', className='custom-tab', selected_className='custom-tab-selected', children=[

                html.Div(id='firstyear-header', children=[
                    html.Div(style={'position': 'relative'}, children=[
                        dcc.Markdown('###### Question \#1', className='tab-title'),
#                     html.Div(
#                         className = 'help help-long help-left',
#                         children = [
#                             dcc.Markdown('''
# Placeholder
#                             '''),
#                             '\u003f\u20dd'
#                         ]
#                     ),
                    ]),
                    html.Div('What year will ', className='tab-text'),
                    html.Div(stations[uid_init]['name'], id='firstyear-header-station', className='tab-text', style={'color': col[0], 'font-weight': 'bold', 'vertical-align': 'middle'}),
                    html.Div('first experience', className='tab-text'),
                    dcc.Dropdown(
                        id = 'numxd-picker',
                        options = fyr_cnts_drpdwn,
                        value = fyrc_init,
                        searchable = False,
                        clearable = False,
                        style = {'height': '35px', 'width': '50px', 'display': 'inline-block', 'margin': '-5px 5px 0px 0px'}
                    ),
                    html.Div('days with sea level exceeding', className='tab-text'),
                    html.Div(str(int(slider_thrsh_init)) + ' cm', id='firstyear-header-threshold', className='tab-text', style={'color': col[0], 'font-weight': 'bold'}),
                    html.Div('above MHHW?', className='tab-text'),
                    html.Details([
                        html.Summary(
                            className = 'read-more-top',
                            style = {'margin-top': '-10px'},
                            children = ['Read more']
                        ),
                        html.Div(
                            className = 'read-more-content',
                            children = [
                                dcc.Markdown('''
Due to the tendency for threshold exceedances to cluster together in a small number of severe years (e.g., [Thompson et al., 2019](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2018JC014741)), a target number of events per year could occur in a single isolated year long before that number becomes the norm. This module allows planners to identify the first year (with associated uncertainty) that a given number of flooding days will occur, which may be useful for defining planning horizons.
                                ''')
                            ]
                        )
                    ]),
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
                    html.Div(style={'position': 'relative'}, children=[
                        dcc.Markdown('###### Question \#2', className='tab-title'),
#                     html.Div(
#                         className = 'help help-long help-left',
#                         children = [
#                             dcc.Markdown('''
# Placeholder
#                             '''),
#                             '\u003f\u20dd'
#                         ]
#                     ),
                    ]),
                    html.Div('When will the frequency of exceedances above the', className='tab-text'),
                    html.Div(str(int(slider_thrsh_init)) + ' cm', id='occ2chrnc-header-threshold', className='tab-text', style={'color': col[0], 'font-weight': 'bold'}),
                    html.Div('threshold transition from occasional to chronic?', className='tab-text'),
                    html.Details([
                        html.Summary(
                            className = 'read-more-top',
                            children = ['Read more']
                        ),
                        html.Div(
                            className = 'read-more-content',
                            children = [
                                dcc.Markdown('''
The length of time between initial, isolated occurences of a given disruptive flood level and routine, chronic disruption is a key variable in planning for the impacts of sea level rise. In this module, *occasional* exceedance is defined to be when 1 in 10 years experiences more than 10 flooding days. *Chronic* excecedance is defined to be when 9 in 10 years experience more than 50 exceedance days, which also roughly corresponds to when 6 in 10 years experience more than 100 exceedance days.

The results of these calculations are concerning, as the transition from occasional to chronic exceedance often occurs rapidly in just 10-15 years, with transitions occurring in less than a decade during the second half of the century. The time-scale of these transitions is essential for planning purposes due to the long lead times needed to develop and fund large-scale infrastructure projects for mitigating the impacts of sea level rise. Thus, it may not be sufficient to wait for a given threshold to be occasionally exceeded before beginning preparedness efforts to mitigate against chronic exceedance.
                                ''')
                            ]
                        )
                    ]),
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

    # -----------------------------------------------------------------------

    html.Details(
        className = 'more-module',
        children = [
            html.Summary(
                className = 'read-more-top',
                children = ['Details of the methodology']
            ),
            html.Div(
                className = 'read-more-content',
                children=[
                    dcc.Markdown('''
---
                    '''),
                    html.Div(className='more-row', children=[
                        dcc.Markdown(className='more-text', children=['''
**Background**

Most people are aware that some high tides are higher than others. The [spring-neap cycle](https://oceanservice.noaa.gov/facts/springtide.html), for example, is related to the alignment of the earth, moon, and sun, and causes tidal amplitude (i.e., the difference between high and low tide) to vary over a lunar month (about 29.5 days). Most people are also aware that sea level rise will cause the highest tides to get even higher and cause flooding thresholds to be exceeded more often (**Figure&nbsp;1**).

However, there are myriad factors across time and space scales that affect how often the ocean height will exceed a given threshold. For example, tidal amplitude does not just vary on a quasi-monthly basis due to the spring-neap cycle; it also varies from season to season and year to year. More specifically, there are substantial 4.4- and 18.6-year cycles in the tides with important implications for the frequency of coastal flooding (e.g., [Haigh et al., 2011](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2010JC006645)). Ocean dynamics also play a role by raising or lowering mean sea level over periods of months or years, with phenomena such as El Ni&ntilde;o (e.g., [Enfield and Allen, 1980](https://journals.ametsoc.org/doi/abs/10.1175/1520-0485%281980%29010%3C0557%3AOTSADO%3E2.0.CO%3B2)) and changes in the strength of the Gulf Stream (e.g., [Sweet et al., 2009](https://tidesandcurrents.noaa.gov/publications/EastCoastSeaLevelAnomaly_2009.pdf)) being two leading factors along the Pacific and Atlantic coastlines of the U.S., respectively. Even without these longer-term fluctuations, changes in storminess or short-term chaotic ocean variability (i.e., ocean "weather") can lead to differences in flooding frequency from one year to the next.

All together, it is possible for multiple factors to "collide" and produce "bursts" of flooding events (e.g., the state-wide, repeated coastal flooding in Hawai`i during summer 2017 discussed by [Thompson et al., 2019](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2018JC014741)). This explains why there are occasional, severe years with many events while other years epxerience few or none at all.

The purpose of this tool is to produce *probablistic* projections of flood frequency in the future that provide information about the full range of possibilities for a given year, including the potential for the occasional&mdash;yet inevitable&mdash;severe years. The projections leverage the predictability inherent in certain contributions (e.g., tidal amplitude and climate-change-induced sea level rise) and use statistical methods to account for everything else. The projections are *probabilistic*, because rather than producing a single, most-likely number of flooding days for a future year, these projections produce a range of plausible numbers with probabilities assigned to each possibility or range of possibilities.
                        ''']),
                        html.Div(
                            className='more-img',
                            id='effect-of-slr-img',
                            children=[
                                html.Img(
                                    src = './assets/effect_of_slr.png'
                                ),
                                dcc.Markdown(className='more-img-caption', children=['''
**Figure 1:** Schematic showing the effect of sea level rise on flooding events. For the same flooding threshold, sea level rise will cause the highest ocean levels to get higher and flooding thresholds to be exceeded more often.
                                '''])
                            ]
                        ),
                    ]),
                    dcc.Markdown('''
---
                    '''),
                    html.Div(className='more-row', children=[
                        dcc.Markdown(className='more-text', children=['''
**Methodology**

The methodology used to produce the projections in this tool is based on the method of [Thompson et al. (2019)](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2018JC014741), which was developed to model future changes in the frequency of high-tide flooding in Honolulu, HI. The method has been generalized and applied to more than 90 locations around the U.S. and its territories for which there is sufficient tide gauge data.

The machinery of the projection algorithm is based around the idea that the probability mass distribution governing the number of threshold exceedances in a given year can be parameterized as a function of the height difference between the threshold of interest and the height of the highest tides of the year. For example, if the threshold is far above the height of the highest tides, then the probability of exceedance is low, and one would expect the probability of zero events to be high with small probabilities of multiple events (**Figure&nbsp;2a**). Alternatively, if the threshold is relatively close to the height of the highest tides, one would expect high probabilities of multiple events with lower probabilities of zero and many events (Figure 2b). In practice, the method employs the flexible [beta-binomial probability mass distribution](https://en.wikipedia.org/wiki/Beta-binomial_distribution) to represent the varying shapes of the distribution as the height of the highest tides varies relative to the height of the threshold. The parameters of the beta-binomial distribution are estimated as functions of the difference between threshold and highest tides on a location-specific basis via an analysis of available tide gauge data.
                        ''']),
                        html.Div(
                            className='more-img',
                            id='distributions-img',
                            children=[
                                html.Img(
                                    src = './assets/distributions.png'
                                ),
                                dcc.Markdown(className='more-img-caption', children=['''
**Figure 2:** Hypothetical probability mass distributions for the number of flooding days per year for two scenarios. (top) The highest astronomical tides are far below the flooding threshold, which means the highest probability is that no flooding days occur. (bottom) The highest astronomical tides are near the flooding threshold, which implies high probability of multiple flooding days.
                                '''])
                            ]
                        ),
                    ]),
                    html.Div(className='more-row', children=[
                        dcc.Markdown(className='more-text', children=['''
Once the parameters of the distribution are established, projections of flooding days requires projections of the highest tides of the year. We define the highest tides of the year as the annual 99th percentile of astronomical tidal variability PLUS annual mean sea level. The latter acts to change the baseline of the tidal variability similar to **Figure&nbsp;1**. In order to project this quantity, we use three ingredients:

* **Ensemble projection of astronomical tidal variability.** This represents an improvement over the methods of [Thompson et al. (2019)](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2018JC014741), which assumed deterministic, stationary tidal constituents. The ensemble tidal projections employed here are based on [Gaussian process](https://en.wikipedia.org/wiki/Gaussian_process) representations of periodic and stochastic variations in the amplitude and phase of major tidal constituents. These projections account for co-variability between certain constituents and mean sea level, as well as trends in tidal amplitude related to non-climatic factors.

* **Ensemble projections of local mean sea level trends and acceleration**. It is essential to use *local* mean sea level projections that incorporate estimates of local and regional vertical land motion, as well as spatial differences in the response of ocean surface height to climate change (e.e., ice melt fingerprints). See the section below *About local mean sea level projections* for more information on the specific projections used.

* **Ensemble projections of stochastic variability in annual mean sea level**. These projections are based on [Gaussian process](https://en.wikipedia.org/wiki/Gaussian_process) representations of unpredictable variations in local annual mean sea level primarily related to atmosphere-ocean dynamics.

The schematic in **Figure&nbsp;3** illustrates how these ingredients are combined into an ensemble prediction of the 99th percentile of tidal height during the 21st century. When further combined with a user defined threshold and parameterizations of the beta-binomial probability mass distribution tuned using tide gauge data, these components produce a probabilistic estimate for the number of flooding days above the threshold in each year.
                        ''']),
                        html.Div(
                            className='more-img',
                            id='schematic-img',
                            children=[
                                html.Img(
                                    src = './assets/schematic.png'
                                ),
                                dcc.Markdown(className='more-img-caption', children=['''
**Figure 3:** Schematic illustrating how various ingredients are combined into an probabilistic projections for the number of flooding days above the threshold during each year of the 21st century.
                                '''])
                            ]
                        ),
                    ]),
                ]
            )
        ]
    ),

    # -----------------------------------------------------------------------

    html.Details(
        className = 'more-module',
        children = [
            html.Summary(
                className = 'read-more-top',
                children = ['About local mean sea level projections']
            ),
            html.Div(
                className = 'read-more-content',
                children=[
                    dcc.Markdown('''
---
                    '''),
                    html.Div(className='more-row', children=[
                        dcc.Markdown(className='more-text', children=['''
The flooding days projections are built on top of projections of local mean sea level. It is absolutely critical to use *localized* mean sea level projections in order to account for local and regional processes such as *ocean dynamics*, *land subsidence*, and *ice melt fingerprints*—all of which cause local sea level rise to differ from the global average rise.

For example, the map in Figure 1 shows twenty-year trends in ocean height across the global ocean from 1993 to 2016. There are large spatial differences with some areas in the western Pacific and Southern Oceans experiencing rates of sea level rise in excess of 1 centimeter per year, while other regions experienced little change or even sea level fall. A majority of the differences in this map are due to ocean-atmosphere dynamics and redistribution of heat in the ocean, but there are a variety of processes that must be considered when making projections for the 21st century.
* Read more about the role of ocean dynamics [**here**] (https://sealevel.nasa.gov/understanding-sea-level/regional-sea-level/ocean-dynamics).
* Read more about land subsidence [**here**] (https://sealevel.nasa.gov/understanding-sea-level/regional-sea-level/subsidence).
* Read more about ice melt fingerprints [**here**](https://sealevel.nasa.gov/understanding-sea-level/regional-sea-level/ice-mass-loss).

Two types of local mean sea level projections are available in this tool. They are described below.
                        ''']),
                        html.Div(
                            className='more-img',
                            id='alt-trend-map-img',
                            children=[
                                html.Img(
                                    src = 'https://sealevel.nasa.gov/internal_resources/185'
                                ),
                                dcc.Markdown(className='more-img-caption', children=['''
**Figure 1:** Twenty-year trends in ocean height across the global ocean from 1993 to 2016. The grids and figure were produced at the Jet Propulsion Laboratory (JPL), California Institute of Technology, under the NASA MEaSUREs program (version JPL 1603). [Data access from PO.DAAC](https://podaac.jpl.nasa.gov/dataset/SEA_SURFACE_HEIGHT_ALT_GRIDS_L4_2SATS_5DAY_6THDEG_V_JPL1609).
                                '''])
                            ]
                        ),
                    ]),

                    dcc.Markdown('''
---
                    '''),
                    html.Div(className='more-row', children=[
                        dcc.Markdown(className='more-text', children=['''
**Kopp et al. (2014) RCP8.5 scenario**

The Kopp et al. projections employed here correspond to the "business as usual" scenario (i.e., the IPCC's RCP8.5 scenario) of greenhouse gas emissions during the 21st century. The global mean sea level projection from Kopp et al. is shown in Figure 2, which gives a 90% probability range for global mean sea level in 2100 under RCP8.5 of roughly 0.5–1.2 meters with a 50th percentile around 0.8 meters.

The *local* mean sea level projections corresponding to this amount of global rise are also probabilistic in nature and account for many sources of local and global uncertainty, giving a realistic view of how uncertainty in local sea level grows in time.

The method used to generate these projections is detailed in an open-access article published in the journal *Earth's Future*. A link to the article is   [**here**](https://tidesandcurrents.noaa.gov/publications/techrpt86_PaP_of_HTFlooding.pdf).
                        ''']),
                        html.Div(
                            className='more-img',
                            id='kopp-scenarios-img',
                            children=[
                                html.Img(
                                    src = 'https://wol-prod-cdn.literatumonline.com/cms/attachment/e7f78669-5ca1-4a5c-95a4-ebd3b11c3161/eft237-fig-0003-m.jpg'
                                ),
                                dcc.Markdown(className='more-img-caption', children=['''
**Figure 2:** Probabilistic global mean sea level rise scenarios from [Kopp et al. (2014)](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2014EF000239) for the three RCPs defined in the IPCC AR5 report. Heavy = median, dashed = 5th–95th percentile, dotted = 0.5th–99.5th percentiles.
                                '''])
                            ]
                        ),
                    ]),
                    dcc.Markdown('''
---
                    '''),
                    html.Div(className='more-row', children=[
                        dcc.Markdown(className='more-text', children=['''
**NOAA Sea Level Rise Scenarios**

These scenarios correspond to plausible sea-level-rise scenarios related to specific amounts of global mean sea level rise (GMSL) experienced by the year 2100. Because they are related to specific end points for GMSL rise by 2100, uncertainty in the projections of flooding days does not grow in time when one of the NOAA scenarios is chosen. The advantage of these scenarios is that it allows the user to define their individual risk tolerance by choosing a specific scenario and then assess impacts based on the implications of that choice (e.g., by looking at the outcomes in this tool).

There are six NOAA scenarios ranging from *low* to *extreme* (Figure 3). Only the three *intermediate* scenarios are used in this tool:
* **Intermediate-low scenario:** 0.5&nbsp;meters (1&nbsp;foot, 8&nbsp;inches) of GMSL rise by 2100.
* **Intermediate scenario:** 1.0&nbsp;meters (3&nbsp;feet, 3&nbsp;inches) of GMSL rise by 2100.
* **Intermediate-high scenario:** 1.5&nbsp;meters (4&nbsp;feet,&nbsp;11 inches) of GMSL rise by 2100.

The method used to create these scenarios is detailed in a NOAA report (Sweet et al., 2017). The report can be accessed [**here**](https://tidesandcurrents.noaa.gov/publications/techrpt83_Global_and_Regional_SLR_Scenarios_for_the_US_final.pdf).
                        ''']),
                        html.Div(
                            className='more-img',
                            id='noaa-scenarios-img',
                            children=[
                                html.Img(
                                    src = 'https://nca2018.globalchange.gov/img/figure/figure2_3.png'
                                ),
                                dcc.Markdown(className='more-img-caption', children=['''
**Figure 3:** The six NOAA global mean sea level rise scenarios, and historical observations of global mean sea level change ([Sweet et al., 2017](https://tidesandcurrents.noaa.gov/publications/techrpt83_Global_and_Regional_SLR_Scenarios_for_the_US_final.pdf)). Image is from the [Fourth National Climate Assessment, Chapter 2](https://nca2018.globalchange.gov/chapter/2/).
                                '''])
                            ]
                        ),
                    ]),
                ]
            )
        ]
    )
])

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# CALLBACKS

# ---------------------------------------------------------------------------
# header

@app.callback(
    dash.dependencies.Output('threshold-slider-value', 'children'),
    [dash.dependencies.Input('threshold-slider', 'value'),
    dash.dependencies.Input('unit-switcher', 'value')]
    )
def update_threshold_slider_value(selected_threshold, units):
    if units == 'in':
        c2i = 0.393701
        selected_threshold = int(np.round(selected_threshold*c2i))
        ustr = ' in'
    else:
        ustr = ' cm'
    return str(selected_threshold) + ustr

@app.callback(
    dash.dependencies.Output('threshold-slider', 'marks'),
    [dash.dependencies.Input('station-picker', 'value'),
    dash.dependencies.Input('unit-switcher', 'value')]
    )
def update_threshold_slider_marks(selected_station, units):

    c2i = 0.393701

    if units == 'cm':
        slider_marks_base = \
            {t: {'label': str(t)} for t in thresholds if t % 10 == 0}
    elif units == 'in':
        slider_marks_base = \
            {t: {'label': str(int(np.round(t*c2i)))}
                for t in thresholds if t*c2i % 3 < 0.4}

    fname = './json/' + selected_station + '/' \
        + 'thresholds.json'
    with open(fname, 'r') as f:
        noaa_thrsh = json.load(f)

    slider_marks_noaa = {
        int(noaa_thrsh['minor']):
            {'label': '\u25B2\nMinor',
                'style': {'color': col[1], 'white-space': 'pre-line'}},
        int(noaa_thrsh['moderate']):
            {'label': '\u25B2\nModerate',
                'style': {'color': col[3], 'white-space': 'pre-line'}},
    }
    slider_marks = {**slider_marks_base, **slider_marks_noaa}

    return slider_marks

@app.callback(
    [dash.dependencies.Output('noaa-thrsh-station', 'children'),
    dash.dependencies.Output('threshold-slider', 'value')],
    [dash.dependencies.Input('station-picker', 'value')]
    )
def update_annual_projections_location_text(selected_station):

    fname = './json/' + selected_station + '/' \
        + 'thresholds.json'
    with open(fname, 'r') as f:
        noaa_thrsh = json.load(f)

    return str(stations[selected_station]['name']), int(noaa_thrsh['minor'])

@app.callback(
    [dash.dependencies.Output('noaa-thrsh-minor', 'children'),
    dash.dependencies.Output('noaa-thrsh-moderate', 'children')],
    [dash.dependencies.Input('station-picker', 'value'),
    dash.dependencies.Input('unit-switcher', 'value')]
    )
def update_moderate_threshold(selected_station, units):

    fname = './json/' + selected_station + '/' \
        + 'thresholds.json'
    with open(fname, 'r') as f:
        noaa_thrsh = json.load(f)

    if units == 'in':
        c2i = 0.393701
        noaa_thrsh['minor'] *= c2i
        noaa_thrsh['moderate'] *= c2i
        ustr = ' in'
    else:
        ustr = ' cm'

    return str(int(np.round(noaa_thrsh['minor']))) + ustr, \
        str(int(np.round(noaa_thrsh['moderate']))) + ustr

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
