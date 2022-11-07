def ap_theme():
    font = 'GoodCompCondBook'
    title_color = '#2c2c2c'
    mark_color = '#174da1'
    return {
        'width':500,
        'height':500,
        'config': {
            'font':font,
            'title': {
                'fontSize': 25,
                'anchor': 'start', 
                'fontColor': title_color,
                'subtitleFontSize':14,
                'subtitleColor':title_color,
                'lineHeight':1.3,
                'subtitleLineHeight':1.3,
                'subtitlePadding':10,
                'subtitleLineHeight':1.3,
                'subtitlePadding':10
            },
            'axisX': {
                'labelFontSize': 12,
                'labelColor':'#b5b5b6',
                'titleFontSize':14,
                'gridDash':[3],
                'gridCap':'round'
            },
            'axisY': {
                'labelFontSize': 12,
                'labelColor':'#b5b5b6',
                'titleFontSize':14,
                'gridDash':[3],
                'gridCap':'round'
            },
            'range': {
               'category': ['#174da1', #cerulean
                    '#78a600', #green 
                    '#a91e75', #magenta
                    '#d8a538', #yellow
                    '#117da5', #blue
                    '#983794', #purple
                    '#df8600', #orange
                    '#b22a20', #red
                    '#00a3a8', #turquoise
                    '#b23a6c'#red-pink
               ],
               'heatmap': [
                   '#feebe2',
                   '#f768a1',
                   '#7a0177'
               ]
            },
            'header' : {
                'labelFontSize':20
            },
            'legend': {
                'labelFontSize': 12,
                'symbolSize': 100, 
                'titleFontSize': 14
            },
            'area': { 
                'fill': mark_color 
            },
            'line': { 
                'stroke': mark_color 
            },
            'bar': {
                'fill':mark_color
            }
        }
    }

import altair as alt

alt.themes.register("ap_theme", ap_theme)
alt.themes.enable("ap_theme")
