PALLET_SPEC = {
    "EURO": [
        {
            "id": "pallet",
            "w": 1.2,
            "d": 0.8,
            "h": 1.4,
            "wg": 22
        }
      ],
    "COMM": [
        {
            "id": "pallet",
            "w": 1.1,
            "d": 1.1,
            "h": 1.42,
            "wg": 11
        }
      ]
}

EURO_PALLET_TG = ['SKIN CUPID LIMITED']

MAX_BOX_D_IN_PALLET = {
    "EURO": {
        'BA10001': 28,
        'BA00023': 28,
        'BA00024': 32,
        'BA00025': 24,
        'BA00026': 32,
        'BA00021': 30,
        'BA00022': 30,
        'BA10022': 30
    },
    "COMM": {
        'BA10001': 42,
        'BA00023': 42,
        'BA00024': 42,
        'BA00025': 36,
        'BA00026': 54,
        'BA00021': 54,
        'BA00022': 54,
        'BA10022': 54
    }
}




MAX_PRDT_D_IN_BOX = {
    'BA10001': 35,
    'BA00023': 35,
    'BA00024': 54,
    'BA00025': 30,
    'BA00026': 77,
    'BA00021': 108,
    'BA00022': 108,
    'BA10022': 108
}

PRDT_SPEC = {
	"BA10001": {
		'WEIGHT': 0.35,
		'SCALE': {
			'WIDTH': 0.06,
			'LENGTH': 0.06,
			'HEIGHT': 0.14
		}
	},
	"BA00023": {
		'WEIGHT': 0.364,
		'SCALE': {
			'WIDTH': 0.06,
			'LENGTH': 0.06,
			'HEIGHT': 0.15
		}
	},
	"BA00024": {
		'WEIGHT': 0.205,
		'SCALE': {
			'WIDTH': 0.05,
			'LENGTH': 0.05,
			'HEIGHT': 0.124
		}
	},
	"BA00025": {
		'WEIGHT': 0.357,
		'SCALE': {
			'WIDTH': 0.087,
			'LENGTH': 0.087,
			'HEIGHT': 0.103
		}
	},
	"BA00026": {
		'WEIGHT': 0.187,
		'SCALE': {
			'WIDTH': 0.044,
			'LENGTH': 0.044,
			'HEIGHT': 0.132
		}
	},
	"BA00021": {
		'WEIGHT': 0.140,
		'SCALE': {
			'WIDTH': 0.054,
			'LENGTH': 0.035,
			'HEIGHT': 0.10
		}
	},
	"BA00022": {
		'WEIGHT': 0.140,
		'SCALE': {
			'WIDTH': 0.054,
			'LENGTH': 0.035,
			'HEIGHT': 0.1
		}
	},
	"BA10022": {
		'WEIGHT': 0.140,
		'SCALE': {
			'WIDTH': 0.054,
			'LENGTH': 0.035,
			'HEIGHT': 0.1
		}
	}
}

BOX_COMM_SPEC = {
	'BOX1': {
		'WEIGHT': 0.5,
		'SCALE': {
			'WIDTH': 0.255,
			'LENGTH': 0.19,
			'HEIGHT': 0.165
		}
	},
	'BOX2': {
		'WEIGHT': 0.5,
		'SCALE': {
			'WIDTH': 0.215,
			'LENGTH': 0.215,
			'HEIGHT': 0.305
		}
	},
	'BOX3': {
		'WEIGHT': 0.5,
		'SCALE': {
			'WIDTH': 0.37,
			'LENGTH': 0.28,
			'HEIGHT': 0.195
		}
	}
}

BOX_D_SPEC = {
    'BA10001': {
          'WEIGHT': 0.75,
          'SCALE': {
            'WIDTH': 0.5,
            'LENGTH': 0.36,
            'HEIGHT': 0.19
          }
    },
    'BA00023': {
          'WEIGHT': 0.92,
          'SCALE': {
            'WIDTH': 0.5,
            'LENGTH': 0.36,
            'HEIGHT': 0.19
          }
    },
    'BA00024': {
          'WEIGHT': 0.73,
          'SCALE': {
            'WIDTH': 0.5,
            'LENGTH': 0.35,
            'HEIGHT': 0.155
          }
    },
    'BA00025': {
          'WEIGHT': 1.05,
          'SCALE': {
            'WIDTH': 0.5,
            'LENGTH': 0.35,
            'HEIGHT': 0.22
          }
    },
    'BA00026': {
          'WEIGHT': 0.78,
          'SCALE': {
            'WIDTH': 0.5,
            'LENGTH': 0.35,
            'HEIGHT': 0.155
          }
    },
    'BA00021': {
          'WEIGHT': 0.38,
          'SCALE': {
            'WIDTH': 0.351,
            'LENGTH': 0.348,
            'HEIGHT': 0.235
          }
    },
    'BA00022': {
          'WEIGHT': 0.38,
          'SCALE': {
            'WIDTH': 0.351,
            'LENGTH': 0.348,
            'HEIGHT': 0.235
          }
    },
    'BA10022': {
          'WEIGHT': 0.38,
          'SCALE': {
            'WIDTH': 0.351,
            'LENGTH': 0.348,
            'HEIGHT': 0.235
          }
    }
  }

BOX_COMM_PRDT_NUM = {
    'BA10001': {
        'BOX1': {
            'MIN_VOLUME': 1,
            'MAX_VOLUME': 12,
        },
        'BOX2': {
            'MIN_VOLUME': 13,
            'MAX_VOLUME': 18,
        }
    },
    'BA00023': {
        'BOX1': {
            'MIN_VOLUME': 1,
            'MAX_VOLUME': 12,
        },
        'BOX2': {
            'MIN_VOLUME': 13,
            'MAX_VOLUME': 18,
        }
    },
    'BA00024': {
        'BOX1': {
            'MIN_VOLUME': 1,
            'MAX_VOLUME': 15,
        },
        'BOX2': {
            'MIN_VOLUME': 16,
            'MAX_VOLUME': 26,
        }
    },
    'BA00025': {
        'BOX1': {
            'MIN_VOLUME': 1,
            'MAX_VOLUME': 4,
        },
        'BOX2': {
            'MIN_VOLUME': 5,
            'MAX_VOLUME': 8,
        },
        'BOX3': {
            'MIN_VOLUME': 9,
            'MAX_VOLUME': 12,
        }
    },
    'BA00026': {
        'BOX1': {
            'MIN_VOLUME': 1,
            'MAX_VOLUME': 20,
        },
        'BOX2': {
            'MIN_VOLUME': 21,
            'MAX_VOLUME': 32,
        },
        'BOX3': {
            'MIN_VOLUME': 33,
            'MAX_VOLUME': 39,
        }
    },
    'BA00021': {
        'BOX1': {
            'MIN_VOLUME': 1,
            'MAX_VOLUME': 20,
        },
        'BOX2': {
            'MIN_VOLUME': 21,
            'MAX_VOLUME': 53,
        }
    },
    'BA00022': {
        'BOX1': {
            'MIN_VOLUME': 1,
            'MAX_VOLUME': 20,
        },
        'BOX2': {
            'MIN_VOLUME': 21,
            'MAX_VOLUME': 53,
        },
    },
    'BA10022': {
        'BOX1': {
            'MIN_VOLUME': 1,
            'MAX_VOLUME': 20,
        },
        'BOX2': {
            'MIN_VOLUME': 21,
            'MAX_VOLUME': 53,
        }
    }
}