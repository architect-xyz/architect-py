/* eslint-disable */
/* prettier-ignore */

export type introspection_types = {
  AberrantFill: {
    kind: 'OBJECT';
    name: 'AberrantFill';
    fields: {
      accountId: {
        name: 'accountId';
        type: { kind: 'SCALAR'; name: 'AccountId'; ofType: null };
      };
      dir: { name: 'dir'; type: { kind: 'SCALAR'; name: 'Dir'; ofType: null } };
      fee: { name: 'fee'; type: { kind: 'OBJECT'; name: 'Fee'; ofType: null } };
      fillId: {
        name: 'fillId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'FillId'; ofType: null };
        };
      };
      isMaker: {
        name: 'isMaker';
        type: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
      };
      kind: {
        name: 'kind';
        type: { kind: 'ENUM'; name: 'FillKind'; ofType: null };
      };
      market: {
        name: 'market';
        type: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
      };
      orderId: {
        name: 'orderId';
        type: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
      };
      price: {
        name: 'price';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      quantity: {
        name: 'quantity';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      recvTime: {
        name: 'recvTime';
        type: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
      };
      tradeTime: {
        name: 'tradeTime';
        type: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
      };
      trader: {
        name: 'trader';
        type: { kind: 'SCALAR'; name: 'UserId'; ofType: null };
      };
    };
  };
  Account: {
    kind: 'OBJECT';
    name: 'Account';
    fields: {
      id: {
        name: 'id';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'AccountId'; ofType: null };
        };
      };
      name: {
        name: 'name';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      venue: {
        name: 'venue';
        type: { kind: 'OBJECT'; name: 'Venue'; ofType: null };
      };
      venueId: {
        name: 'venueId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'VenueId'; ofType: null };
        };
      };
    };
  };
  AccountId: unknown;
  AccountSummaries: {
    kind: 'OBJECT';
    name: 'AccountSummaries';
    fields: {
      byAccount: {
        name: 'byAccount';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'AccountSummary'; ofType: null };
            };
          };
        };
      };
      snapshotTs: {
        name: 'snapshotTs';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
    };
  };
  AccountSummary: {
    kind: 'OBJECT';
    name: 'AccountSummary';
    fields: {
      account: {
        name: 'account';
        type: { kind: 'OBJECT'; name: 'Account'; ofType: null };
      };
      accountId: {
        name: 'accountId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'AccountId'; ofType: null };
        };
      };
      balances: {
        name: 'balances';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'Balance'; ofType: null };
            };
          };
        };
      };
      positions: {
        name: 'positions';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'Position'; ofType: null };
            };
          };
        };
      };
      profitLoss: {
        name: 'profitLoss';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      venue: {
        name: 'venue';
        type: { kind: 'OBJECT'; name: 'Venue'; ofType: null };
      };
      venueId: {
        name: 'venueId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'VenueId'; ofType: null };
        };
      };
    };
  };
  Ack: {
    kind: 'OBJECT';
    name: 'Ack';
    fields: {
      order: {
        name: 'order';
        type: { kind: 'OBJECT'; name: 'Order'; ofType: null };
      };
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
    };
  };
  AlgoControlCommand: {
    name: 'AlgoControlCommand';
    enumValues: 'PAUSE' | 'START' | 'STOP';
  };
  AlgoKind: {
    name: 'AlgoKind';
    enumValues:
      | 'CHASER'
      | 'MARKET_MAKER'
      | 'POV'
      | 'SMART_ORDER_ROUTER'
      | 'SPREAD'
      | 'TWAP';
  };
  AlgoLog: {
    kind: 'OBJECT';
    name: 'AlgoLog';
    fields: {
      aberrantFills: {
        name: 'aberrantFills';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'AberrantFill'; ofType: null };
            };
          };
        };
      };
      fills: {
        name: 'fills';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'Fill'; ofType: null };
            };
          };
        };
      };
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      rejects: {
        name: 'rejects';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'Reject'; ofType: null };
            };
          };
        };
      };
    };
  };
  AlgoOrder: {
    kind: 'OBJECT';
    name: 'AlgoOrder';
    fields: {
      account: {
        name: 'account';
        type: { kind: 'SCALAR'; name: 'AccountId'; ofType: null };
      };
      algo: {
        name: 'algo';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'ENUM'; name: 'AlgoKind'; ofType: null };
        };
      };
      markets: {
        name: 'markets';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
            };
          };
        };
      };
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      parentOrderId: {
        name: 'parentOrderId';
        type: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
      };
      trader: {
        name: 'trader';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'UserId'; ofType: null };
        };
      };
    };
  };
  AlgoPreview: {
    kind: 'OBJECT';
    name: 'AlgoPreview';
    fields: {
      orders: {
        name: 'orders';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'Order'; ofType: null };
            };
          };
        };
      };
    };
  };
  AlgoRunningStatus: {
    name: 'AlgoRunningStatus';
    enumValues: 'DONE' | 'PAUSED' | 'RUNNING';
  };
  AlgoStatus: {
    kind: 'OBJECT';
    name: 'AlgoStatus';
    fields: {
      creationTime: {
        name: 'creationTime';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
      fractionComplete: {
        name: 'fractionComplete';
        type: { kind: 'SCALAR'; name: 'Float'; ofType: null };
      };
      lastStatusChange: {
        name: 'lastStatusChange';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
      order: {
        name: 'order';
        type: { kind: 'OBJECT'; name: 'AlgoOrder'; ofType: null };
      };
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      status: {
        name: 'status';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'ENUM'; name: 'AlgoRunningStatus'; ofType: null };
        };
      };
    };
  };
  ApiKey: {
    kind: 'OBJECT';
    name: 'ApiKey';
    fields: {
      apiKey: {
        name: 'apiKey';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      apiSecret: {
        name: 'apiSecret';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      created: {
        name: 'created';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
      subject: {
        name: 'subject';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
    };
  };
  Balance: {
    kind: 'OBJECT';
    name: 'Balance';
    fields: {
      account: {
        name: 'account';
        type: { kind: 'OBJECT'; name: 'Account'; ofType: null };
      };
      accountId: {
        name: 'accountId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'AccountId'; ofType: null };
        };
      };
      amount: {
        name: 'amount';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      cashExcess: {
        name: 'cashExcess';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      marginExcess: {
        name: 'marginExcess';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      positionMargin: {
        name: 'positionMargin';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      product: {
        name: 'product';
        type: { kind: 'OBJECT'; name: 'Product'; ofType: null };
      };
      productId: {
        name: 'productId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'ProductId'; ofType: null };
        };
      };
      purchasingPower: {
        name: 'purchasingPower';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      totalMargin: {
        name: 'totalMargin';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      venue: {
        name: 'venue';
        type: { kind: 'OBJECT'; name: 'Venue'; ofType: null };
      };
      venueId: {
        name: 'venueId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'VenueId'; ofType: null };
        };
      };
      yesterdayBalance: {
        name: 'yesterdayBalance';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
    };
  };
  Book: {
    kind: 'OBJECT';
    name: 'Book';
    fields: {
      asks: {
        name: 'asks';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'BookLevel'; ofType: null };
            };
          };
        };
      };
      bids: {
        name: 'bids';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'BookLevel'; ofType: null };
            };
          };
        };
      };
      market: {
        name: 'market';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
      };
      timestamp: {
        name: 'timestamp';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
    };
  };
  BookLevel: {
    kind: 'OBJECT';
    name: 'BookLevel';
    fields: {
      amount: {
        name: 'amount';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      price: {
        name: 'price';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      total: {
        name: 'total';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
    };
  };
  Boolean: unknown;
  Cancel: {
    kind: 'OBJECT';
    name: 'Cancel';
    fields: {
      order: {
        name: 'order';
        type: { kind: 'OBJECT'; name: 'Order'; ofType: null };
      };
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
    };
  };
  CancelAll: {
    kind: 'OBJECT';
    name: 'CancelAll';
    fields: {
      venueId: {
        name: 'venueId';
        type: { kind: 'SCALAR'; name: 'VenueId'; ofType: null };
      };
    };
  };
  CandleV1: {
    kind: 'OBJECT';
    name: 'CandleV1';
    fields: {
      buyVolume: {
        name: 'buyVolume';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      close: {
        name: 'close';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      high: {
        name: 'high';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      low: {
        name: 'low';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      open: {
        name: 'open';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      sellVolume: {
        name: 'sellVolume';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      time: {
        name: 'time';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
      volume: {
        name: 'volume';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
    };
  };
  CandleWidth: {
    name: 'CandleWidth';
    enumValues:
      | 'FIFTEEN_MINUTE'
      | 'FIVE_SECOND'
      | 'ONE_DAY'
      | 'ONE_HOUR'
      | 'ONE_MINUTE'
      | 'ONE_SECOND';
  };
  CmeProductGroupInfo: {
    kind: 'OBJECT';
    name: 'CmeProductGroupInfo';
    fields: {
      altGlobexMinTick: {
        name: 'altGlobexMinTick';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      altGlobexTickConstraint: {
        name: 'altGlobexTickConstraint';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      altMinQuoteLife: {
        name: 'altMinQuoteLife';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      assetClass: {
        name: 'assetClass';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      assetSubClass: {
        name: 'assetSubClass';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      assignmentMethod: {
        name: 'assignmentMethod';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      blockTradeEligible: {
        name: 'blockTradeEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      calendarTickRules: {
        name: 'calendarTickRules';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      category: {
        name: 'category';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      clearingCabPx: {
        name: 'clearingCabPx';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      clearingOrgId: {
        name: 'clearingOrgId';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      clearingSymbol: {
        name: 'clearingSymbol';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      clearportEligible: {
        name: 'clearportEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      clearportSchedule: {
        name: 'clearportSchedule';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      commodityStandards: {
        name: 'commodityStandards';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      contractNotionalAmount: {
        name: 'contractNotionalAmount';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      contraryInstructionsAllowed: {
        name: 'contraryInstructionsAllowed';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      dailyFlag: {
        name: 'dailyFlag';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      daysOrHours: {
        name: 'daysOrHours';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      defaultListingRules: {
        name: 'defaultListingRules';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      defaultMinTick: {
        name: 'defaultMinTick';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      dirtyPriceRounding: {
        name: 'dirtyPriceRounding';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      dirtyPriceTick: {
        name: 'dirtyPriceTick';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      ebfEligible: {
        name: 'ebfEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      efpEligible: {
        name: 'efpEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      efrEligible: {
        name: 'efrEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      exchangeClearing: {
        name: 'exchangeClearing';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      exchangeGlobex: {
        name: 'exchangeGlobex';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      exerciseStyle: {
        name: 'exerciseStyle';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      exerciseStyleAmericanEuropean: {
        name: 'exerciseStyleAmericanEuropean';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      fixedPayout: {
        name: 'fixedPayout';
        type: { kind: 'SCALAR'; name: 'Float'; ofType: null };
      };
      fixingSource: {
        name: 'fixingSource';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      fixingTimeZone: {
        name: 'fixingTimeZone';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      flexEligible: {
        name: 'flexEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      floorCallSymbol: {
        name: 'floorCallSymbol';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      floorEligible: {
        name: 'floorEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      floorListingRules: {
        name: 'floorListingRules';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      floorPutSymbol: {
        name: 'floorPutSymbol';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      floorSchedule: {
        name: 'floorSchedule';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      fractional: {
        name: 'fractional';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      gcBasketIdentifier: {
        name: 'gcBasketIdentifier';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      globexCabPx: {
        name: 'globexCabPx';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      globexDisplayFactor: {
        name: 'globexDisplayFactor';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      globexEligible: {
        name: 'globexEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      globexGroupCode: {
        name: 'globexGroupCode';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      globexGroupDescr: {
        name: 'globexGroupDescr';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      globexGtEligible: {
        name: 'globexGtEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      globexListingRules: {
        name: 'globexListingRules';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      globexMatchAlgo: {
        name: 'globexMatchAlgo';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      globexMinTick: {
        name: 'globexMinTick';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      globexProductCode: {
        name: 'globexProductCode';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      globexSchedule: {
        name: 'globexSchedule';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      goodForSession: {
        name: 'goodForSession';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      ilinkEligible: {
        name: 'ilinkEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      isBticProduct: {
        name: 'isBticProduct';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      isDerivedBlockEligible: {
        name: 'isDerivedBlockEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      isEfixProduct: {
        name: 'isEfixProduct';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      isPmEligible: {
        name: 'isPmEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      isSyntheticProduct: {
        name: 'isSyntheticProduct';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      isTacoProduct: {
        name: 'isTacoProduct';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      isTamProduct: {
        name: 'isTamProduct';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      isTasProduct: {
        name: 'isTasProduct';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      isTmacProduct: {
        name: 'isTmacProduct';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      itcCode: {
        name: 'itcCode';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      itmOtm: {
        name: 'itmOtm';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      lastDeliveryRules: {
        name: 'lastDeliveryRules';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      lastUpdated: {
        name: 'lastUpdated';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      limitRules: {
        name: 'limitRules';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      mainFraction: {
        name: 'mainFraction';
        type: { kind: 'SCALAR'; name: 'Int'; ofType: null };
      };
      markerStlmtRules: {
        name: 'markerStlmtRules';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      marketData: {
        name: 'marketData';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      marketSegmentId: {
        name: 'marketSegmentId';
        type: { kind: 'SCALAR'; name: 'Int'; ofType: null };
      };
      massQuoteEligible: {
        name: 'massQuoteEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      masterSymbol: {
        name: 'masterSymbol';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      maxBidAskConstraint: {
        name: 'maxBidAskConstraint';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      maxGlobexOrdQty: {
        name: 'maxGlobexOrdQty';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      mdp3Channel: {
        name: 'mdp3Channel';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      midcurveOptionsRules: {
        name: 'midcurveOptionsRules';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      midcurveTickRules: {
        name: 'midcurveTickRules';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      minCabinetTickRules: {
        name: 'minCabinetTickRules';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      minClearportFloorTick: {
        name: 'minClearportFloorTick';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      minClearportTick: {
        name: 'minClearportTick';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      minDaysToMat: {
        name: 'minDaysToMat';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      minGlobexOrdQty: {
        name: 'minGlobexOrdQty';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      minIncrementalOrder: {
        name: 'minIncrementalOrder';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      minOutrightTick: {
        name: 'minOutrightTick';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      minQtrlySerialTick: {
        name: 'minQtrlySerialTick';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      minimumHalfTick: {
        name: 'minimumHalfTick';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      minimumTickNote: {
        name: 'minimumTickNote';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      negativePxEligible: {
        name: 'negativePxEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      negativeStrikeEligible: {
        name: 'negativeStrikeEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      onMtf: {
        name: 'onMtf';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      onSef: {
        name: 'onSef';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      optStyle: {
        name: 'optStyle';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      otcEligible: {
        name: 'otcEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      parOrMoney: {
        name: 'parOrMoney';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      priceBand: {
        name: 'priceBand';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      priceMultiplier: {
        name: 'priceMultiplier';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      pricePrecision: {
        name: 'pricePrecision';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      priceQuotation: {
        name: 'priceQuotation';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      productGuid: {
        name: 'productGuid';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      productName: {
        name: 'productName';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      pxQuoteMethod: {
        name: 'pxQuoteMethod';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      pxUnitOfMeasure: {
        name: 'pxUnitOfMeasure';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      pxUnitOfMeasureQty: {
        name: 'pxUnitOfMeasureQty';
        type: { kind: 'SCALAR'; name: 'Int'; ofType: null };
      };
      quarterlyListingRules: {
        name: 'quarterlyListingRules';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      rbtEligibleInd: {
        name: 'rbtEligibleInd';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      reducedTickNotes: {
        name: 'reducedTickNotes';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      regularListingRules: {
        name: 'regularListingRules';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      repoYearDays: {
        name: 'repoYearDays';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      reportablePositions: {
        name: 'reportablePositions';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      rfqCrossEligible: {
        name: 'rfqCrossEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      sector: {
        name: 'sector';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      securityType: {
        name: 'securityType';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'ENUM'; name: 'CmeSecurityType'; ofType: null };
        };
      };
      serialListingRules: {
        name: 'serialListingRules';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      settlCcy: {
        name: 'settlCcy';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      settleMethod: {
        name: 'settleMethod';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      settlePxCcy: {
        name: 'settlePxCcy';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      settleUsingFixingPx: {
        name: 'settleUsingFixingPx';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      settlementAtExpiration: {
        name: 'settlementAtExpiration';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      settlementLocale: {
        name: 'settlementLocale';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      settlementProcedure: {
        name: 'settlementProcedure';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      settlementType: {
        name: 'settlementType';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      sizePriorityQty: {
        name: 'sizePriorityQty';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      spreadPricingConvention: {
        name: 'spreadPricingConvention';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      stdTradingHours: {
        name: 'stdTradingHours';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      strategyType: {
        name: 'strategyType';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      strikePriceInterval: {
        name: 'strikePriceInterval';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      subCategory: {
        name: 'subCategory';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      subSector: {
        name: 'subSector';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      subfraction: {
        name: 'subfraction';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      subtype: {
        name: 'subtype';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      topEligible: {
        name: 'topEligible';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      totClearport: {
        name: 'totClearport';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      totDefault: {
        name: 'totDefault';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      totFloor: {
        name: 'totFloor';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      totGlobex: {
        name: 'totGlobex';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      totLtd: {
        name: 'totLtd';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      totMidcurve: {
        name: 'totMidcurve';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      totQuarterly: {
        name: 'totQuarterly';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      totSerial: {
        name: 'totSerial';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      tradeCloseOffSet: {
        name: 'tradeCloseOffSet';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      tradePxCcy: {
        name: 'tradePxCcy';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      tradingCutOffTime: {
        name: 'tradingCutOffTime';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      unitOfMeasure: {
        name: 'unitOfMeasure';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      unitOfMeasureQty: {
        name: 'unitOfMeasureQty';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      url: {
        name: 'url';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      valuationMethod: {
        name: 'valuationMethod';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      varCabPxHigh: {
        name: 'varCabPxHigh';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      varCabPxLow: {
        name: 'varCabPxLow';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      variableQtyFlag: {
        name: 'variableQtyFlag';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
    };
  };
  CmeSecurityType: {
    name: 'CmeSecurityType';
    enumValues:
      | 'CASH'
      | 'COMBO'
      | 'FRA'
      | 'FUT'
      | 'FWD'
      | 'IDX'
      | 'INDEX'
      | 'IRS'
      | 'OOC'
      | 'OOF';
  };
  CoinInfo: {
    kind: 'OBJECT';
    name: 'CoinInfo';
    fields: {
      circulatingSupply: {
        name: 'circulatingSupply';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      fullyDilutedMarketCap: {
        name: 'fullyDilutedMarketCap';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      infiniteSupply: {
        name: 'infiniteSupply';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
        };
      };
      marketCap: {
        name: 'marketCap';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      maxSupply: {
        name: 'maxSupply';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      name: {
        name: 'name';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      percentChange1h: {
        name: 'percentChange1h';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      percentChange24h: {
        name: 'percentChange24h';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      percentChange30d: {
        name: 'percentChange30d';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      percentChange60d: {
        name: 'percentChange60d';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      percentChange7d: {
        name: 'percentChange7d';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      percentChange90d: {
        name: 'percentChange90d';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      price: {
        name: 'price';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      symbol: {
        name: 'symbol';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      tags: {
        name: 'tags';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
            };
          };
        };
      };
      totalSupply: {
        name: 'totalSupply';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      volume24h: {
        name: 'volume24h';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      volumeChange24h: {
        name: 'volumeChange24h';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
    };
  };
  ComponentId: string;
  CptyInfo: {
    kind: 'OBJECT';
    name: 'CptyInfo';
    fields: {
      canSetCredentials: {
        name: 'canSetCredentials';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
        };
      };
      componentId: {
        name: 'componentId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'ComponentId'; ofType: null };
        };
      };
      route: {
        name: 'route';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Route'; ofType: null };
        };
      };
      venue: {
        name: 'venue';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Venue'; ofType: null };
        };
      };
    };
  };
  CreateMMAlgo: {
    kind: 'INPUT_OBJECT';
    name: 'CreateMMAlgo';
    isOneOf: false;
    inputFields: [
      {
        name: 'account';
        type: { kind: 'SCALAR'; name: 'AccountId'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'buyQuantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'fillLockoutMs';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Int'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'market';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'maxImproveBbo';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'maxPosition';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'minPosition';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'name';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Str'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'orderLockoutMs';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Int'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'positionTilt';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'refDistFrac';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'referencePrice';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'ENUM'; name: 'ReferencePrice'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'rejectLockoutMs';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Int'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'sellQuantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'toleranceFrac';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
    ];
  };
  CreateOrder: {
    kind: 'INPUT_OBJECT';
    name: 'CreateOrder';
    isOneOf: false;
    inputFields: [
      {
        name: 'account';
        type: { kind: 'SCALAR'; name: 'AccountId'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'dir';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Dir'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'limitPrice';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'market';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'orderType';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'ENUM'; name: 'CreateOrderType'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'postOnly';
        type: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'quantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'quoteId';
        type: { kind: 'SCALAR'; name: 'Str'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'source';
        type: { kind: 'ENUM'; name: 'OrderSource'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'timeInForce';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'INPUT_OBJECT';
            name: 'CreateTimeInForce';
            ofType: null;
          };
        };
        defaultValue: null;
      },
      {
        name: 'triggerPrice';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        defaultValue: null;
      },
    ];
  };
  CreateOrderType: {
    name: 'CreateOrderType';
    enumValues: 'LIMIT' | 'STOP_LOSS_LIMIT' | 'TAKE_PROFIT_LIMIT';
  };
  CreatePovAlgo: {
    kind: 'INPUT_OBJECT';
    name: 'CreatePovAlgo';
    isOneOf: false;
    inputFields: [
      {
        name: 'account';
        type: { kind: 'SCALAR'; name: 'AccountId'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'dir';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Dir'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'endTime';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'market';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'maxQuantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'minOrderQuantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'name';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Str'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'orderLockoutMs';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Int'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'takeThroughFrac';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'targetVolumeFrac';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
    ];
  };
  CreateSmartOrderRouterAlgo: {
    kind: 'INPUT_OBJECT';
    name: 'CreateSmartOrderRouterAlgo';
    isOneOf: false;
    inputFields: [
      {
        name: 'base';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'ProductId'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'dir';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Dir'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'executionTimeLimitMs';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Int'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'limitPrice';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'markets';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
            };
          };
        };
        defaultValue: null;
      },
      {
        name: 'quote';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'ProductId'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'targetSize';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
    ];
  };
  CreateSpreadAlgo: {
    kind: 'INPUT_OBJECT';
    name: 'CreateSpreadAlgo';
    isOneOf: false;
    inputFields: [
      {
        name: 'account';
        type: { kind: 'SCALAR'; name: 'AccountId'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'buyQuantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'fillLockoutMs';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Int'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'hedgeMarket';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'INPUT_OBJECT';
            name: 'CreateSpreadAlgoHedgeMarket';
            ofType: null;
          };
        };
        defaultValue: null;
      },
      {
        name: 'market';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'maxImproveBbo';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'maxPosition';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'minPosition';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'name';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Str'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'orderLockoutMs';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Int'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'positionTilt';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'refDistFrac';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'referencePrice';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'ENUM'; name: 'ReferencePrice'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'rejectLockoutMs';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Int'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'sellQuantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'toleranceFrac';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
    ];
  };
  CreateSpreadAlgoHedgeMarket: {
    kind: 'INPUT_OBJECT';
    name: 'CreateSpreadAlgoHedgeMarket';
    isOneOf: false;
    inputFields: [
      {
        name: 'conversionRatio';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'hedgeFrac';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'market';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'premium';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
    ];
  };
  CreateTimeInForce: {
    kind: 'INPUT_OBJECT';
    name: 'CreateTimeInForce';
    isOneOf: false;
    inputFields: [
      {
        name: 'goodTilDate';
        type: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'instruction';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'ENUM';
            name: 'CreateTimeInForceInstruction';
            ofType: null;
          };
        };
        defaultValue: null;
      },
    ];
  };
  CreateTimeInForceInstruction: {
    name: 'CreateTimeInForceInstruction';
    enumValues: 'GTC' | 'GTD' | 'IOC';
  };
  CreateTwapAlgo: {
    kind: 'INPUT_OBJECT';
    name: 'CreateTwapAlgo';
    isOneOf: false;
    inputFields: [
      {
        name: 'account';
        type: { kind: 'SCALAR'; name: 'AccountId'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'dir';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Dir'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'endTime';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'intervalMs';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Int'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'market';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'name';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Str'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'quantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'rejectLockoutMs';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Int'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'takeThroughFrac';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        defaultValue: null;
      },
    ];
  };
  Date: string;
  DateTime: string;
  Decimal: string;
  Dir: string;
  Environment: {
    kind: 'OBJECT';
    name: 'Environment';
    fields: {
      id: {
        name: 'id';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      kind: {
        name: 'kind';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'ENUM'; name: 'EnvironmentKind'; ofType: null };
        };
      };
    };
  };
  EnvironmentKind: {
    name: 'EnvironmentKind';
    enumValues: 'BROKERAGE' | 'PLATFORM';
  };
  ExchangeMarketKind: {
    kind: 'OBJECT';
    name: 'ExchangeMarketKind';
    fields: {
      base: {
        name: 'base';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Product'; ofType: null };
        };
      };
      quote: {
        name: 'quote';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Product'; ofType: null };
        };
      };
    };
  };
  ExchangeSpecificUpdate: {
    kind: 'OBJECT';
    name: 'ExchangeSpecificUpdate';
    fields: {
      field: {
        name: 'field';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      market: {
        name: 'market';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Market'; ofType: null };
        };
      };
      value: {
        name: 'value';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
    };
  };
  Fee: {
    kind: 'OBJECT';
    name: 'Fee';
    fields: {
      amount: {
        name: 'amount';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      feeCurrency: {
        name: 'feeCurrency';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'ProductId'; ofType: null };
        };
      };
    };
  };
  Fill: {
    kind: 'OBJECT';
    name: 'Fill';
    fields: {
      dir: {
        name: 'dir';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Dir'; ofType: null };
        };
      };
      fillId: {
        name: 'fillId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'FillId'; ofType: null };
        };
      };
      kind: {
        name: 'kind';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'ENUM'; name: 'FillKind'; ofType: null };
        };
      };
      market: {
        name: 'market';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Market'; ofType: null };
        };
      };
      marketId: {
        name: 'marketId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
      };
      orderId: {
        name: 'orderId';
        type: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
      };
      price: {
        name: 'price';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      quantity: {
        name: 'quantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      recvTime: {
        name: 'recvTime';
        type: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
      };
      tradeTime: {
        name: 'tradeTime';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
    };
  };
  FillId: string;
  FillKind: {
    name: 'FillKind';
    enumValues: 'CORRECTION' | 'NORMAL' | 'REVERSAL';
  };
  Fills: {
    kind: 'OBJECT';
    name: 'Fills';
    fields: {
      aberrant: {
        name: 'aberrant';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'AberrantFill'; ofType: null };
            };
          };
        };
      };
      normal: {
        name: 'normal';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'Fill'; ofType: null };
            };
          };
        };
      };
    };
  };
  Float: string;
  HedgeMarket: {
    kind: 'OBJECT';
    name: 'HedgeMarket';
    fields: {
      conversionRatio: {
        name: 'conversionRatio';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      hedgeFrac: {
        name: 'hedgeFrac';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      market: {
        name: 'market';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
      };
      premium: {
        name: 'premium';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
    };
  };
  Int: string;
  License: {
    kind: 'OBJECT';
    name: 'License';
    fields: {
      expiry: {
        name: 'expiry';
        type: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
      };
      tier: {
        name: 'tier';
        type: { kind: 'ENUM'; name: 'LicenseTier'; ofType: null };
      };
      user: {
        name: 'user';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'UserId'; ofType: null };
        };
      };
    };
  };
  LicenseTier: { name: 'LicenseTier'; enumValues: 'BASIC' | 'PROFESSIONAL' };
  LimitOrderType: {
    kind: 'OBJECT';
    name: 'LimitOrderType';
    fields: {
      limitPrice: {
        name: 'limitPrice';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      postOnly: {
        name: 'postOnly';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
        };
      };
    };
  };
  MMAlgoDecision: {
    kind: 'UNION';
    name: 'MMAlgoDecision';
    fields: {};
    possibleTypes:
      | 'MMAlgoDecisionCancel'
      | 'MMAlgoDecisionDoNothing'
      | 'MMAlgoDecisionSend';
  };
  MMAlgoDecisionCancel: {
    kind: 'OBJECT';
    name: 'MMAlgoDecisionCancel';
    fields: {
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      reasons: {
        name: 'reasons';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'ENUM'; name: 'Reason'; ofType: null };
            };
          };
        };
      };
    };
  };
  MMAlgoDecisionDoNothing: {
    kind: 'OBJECT';
    name: 'MMAlgoDecisionDoNothing';
    fields: {
      reasons: {
        name: 'reasons';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'ENUM'; name: 'Reason'; ofType: null };
            };
          };
        };
      };
    };
  };
  MMAlgoDecisionSend: {
    kind: 'OBJECT';
    name: 'MMAlgoDecisionSend';
    fields: {
      price: {
        name: 'price';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      quantity: {
        name: 'quantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
    };
  };
  MMAlgoKind: { name: 'MMAlgoKind'; enumValues: 'MM' | 'SPREAD' };
  MMAlgoOpenOrder: {
    kind: 'OBJECT';
    name: 'MMAlgoOpenOrder';
    fields: {
      cancelPending: {
        name: 'cancelPending';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
        };
      };
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      price: {
        name: 'price';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      quantity: {
        name: 'quantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
    };
  };
  MMAlgoOrder: {
    kind: 'OBJECT';
    name: 'MMAlgoOrder';
    fields: {
      account: {
        name: 'account';
        type: { kind: 'SCALAR'; name: 'AccountId'; ofType: null };
      };
      hedgeMarket: {
        name: 'hedgeMarket';
        type: { kind: 'OBJECT'; name: 'HedgeMarket'; ofType: null };
      };
      market: {
        name: 'market';
        type: { kind: 'OBJECT'; name: 'Market'; ofType: null };
      };
      marketId: {
        name: 'marketId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
      };
      maxImproveBbo: {
        name: 'maxImproveBbo';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      maxPosition: {
        name: 'maxPosition';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      minPosition: {
        name: 'minPosition';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      name: {
        name: 'name';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      positionTilt: {
        name: 'positionTilt';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      quantityBuy: {
        name: 'quantityBuy';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      quantitySell: {
        name: 'quantitySell';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      refDistFrac: {
        name: 'refDistFrac';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      referencePrice: {
        name: 'referencePrice';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'ENUM'; name: 'ReferencePrice'; ofType: null };
        };
      };
      toleranceFrac: {
        name: 'toleranceFrac';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
    };
  };
  MMAlgoSide: {
    kind: 'OBJECT';
    name: 'MMAlgoSide';
    fields: {
      lastDecision: {
        name: 'lastDecision';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'UNION'; name: 'MMAlgoDecision'; ofType: null };
        };
      };
      lastFillTime: {
        name: 'lastFillTime';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
      lastOrderTime: {
        name: 'lastOrderTime';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
      lastRejectTime: {
        name: 'lastRejectTime';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
      openOrder: {
        name: 'openOrder';
        type: { kind: 'OBJECT'; name: 'MMAlgoOpenOrder'; ofType: null };
      };
      referencePrice: {
        name: 'referencePrice';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
    };
  };
  MMAlgoStatus: {
    kind: 'OBJECT';
    name: 'MMAlgoStatus';
    fields: {
      buyStatus: {
        name: 'buyStatus';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'MMAlgoSide'; ofType: null };
        };
      };
      creationTime: {
        name: 'creationTime';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
      effectiveSpread: {
        name: 'effectiveSpread';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      hedgePosition: {
        name: 'hedgePosition';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      kind: {
        name: 'kind';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'ENUM'; name: 'MMAlgoKind'; ofType: null };
        };
      };
      missRatio: {
        name: 'missRatio';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      order: {
        name: 'order';
        type: { kind: 'OBJECT'; name: 'MMAlgoOrder'; ofType: null };
      };
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      position: {
        name: 'position';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      sellStatus: {
        name: 'sellStatus';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'MMAlgoSide'; ofType: null };
        };
      };
      status: {
        name: 'status';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'ENUM'; name: 'AlgoRunningStatus'; ofType: null };
        };
      };
    };
  };
  Market: {
    kind: 'OBJECT';
    name: 'Market';
    fields: {
      cmeProductGroupInfo: {
        name: 'cmeProductGroupInfo';
        type: { kind: 'OBJECT'; name: 'CmeProductGroupInfo'; ofType: null };
      };
      exchangeSymbol: {
        name: 'exchangeSymbol';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      firstNoticeDate: {
        name: 'firstNoticeDate';
        type: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
      };
      id: {
        name: 'id';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
      };
      initialMargin: {
        name: 'initialMargin';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      isDelisted: {
        name: 'isDelisted';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
        };
      };
      isFavorite: {
        name: 'isFavorite';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
        };
      };
      kind: {
        name: 'kind';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'UNION'; name: 'MarketKind'; ofType: null };
        };
      };
      lastTradingDate: {
        name: 'lastTradingDate';
        type: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
      };
      maintenanceMargin: {
        name: 'maintenanceMargin';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      minOrderQuantity: {
        name: 'minOrderQuantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      minOrderQuantityUnit: {
        name: 'minOrderQuantityUnit';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'ENUM'; name: 'MinOrderQuantityUnit'; ofType: null };
        };
      };
      name: {
        name: 'name';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      route: {
        name: 'route';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Route'; ofType: null };
        };
      };
      stepSize: {
        name: 'stepSize';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      tickSize: {
        name: 'tickSize';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      venue: {
        name: 'venue';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Venue'; ofType: null };
        };
      };
    };
  };
  MarketFilter: {
    kind: 'INPUT_OBJECT';
    name: 'MarketFilter';
    isOneOf: false;
    inputFields: [
      {
        name: 'base';
        type: { kind: 'SCALAR'; name: 'Str'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'includeDelisted';
        type: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'maxResults';
        type: { kind: 'SCALAR'; name: 'Int'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'onlyFavorites';
        type: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'quote';
        type: { kind: 'SCALAR'; name: 'Str'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'resultsOffset';
        type: { kind: 'SCALAR'; name: 'Int'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'route';
        type: { kind: 'SCALAR'; name: 'Str'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'searchString';
        type: { kind: 'SCALAR'; name: 'Str'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'sortByVolumeDesc';
        type: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'underlying';
        type: { kind: 'SCALAR'; name: 'Str'; ofType: null };
        defaultValue: null;
      },
      {
        name: 'venue';
        type: { kind: 'SCALAR'; name: 'Str'; ofType: null };
        defaultValue: null;
      },
    ];
  };
  MarketId: string;
  MarketKind: {
    kind: 'UNION';
    name: 'MarketKind';
    fields: {};
    possibleTypes:
      | 'ExchangeMarketKind'
      | 'PoolMarketKind'
      | 'UnknownMarketKind';
  };
  MarketSnapshot: {
    kind: 'OBJECT';
    name: 'MarketSnapshot';
    fields: {
      askPrice: {
        name: 'askPrice';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      bidPrice: {
        name: 'bidPrice';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      high24h: {
        name: 'high24h';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      lastPrice: {
        name: 'lastPrice';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      low24h: {
        name: 'low24h';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      market: {
        name: 'market';
        type: { kind: 'OBJECT'; name: 'Market'; ofType: null };
      };
      marketId: {
        name: 'marketId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
      };
      open24h: {
        name: 'open24h';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      volume24h: {
        name: 'volume24h';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
    };
  };
  Me: {
    kind: 'OBJECT';
    name: 'Me';
    fields: {
      email: {
        name: 'email';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      environment: {
        name: 'environment';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Environment'; ofType: null };
        };
      };
      isStaff: {
        name: 'isStaff';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
        };
      };
      license: {
        name: 'license';
        type: { kind: 'OBJECT'; name: 'License'; ofType: null };
      };
      userId: {
        name: 'userId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'UserId'; ofType: null };
        };
      };
    };
  };
  MinOrderQuantityUnit: {
    name: 'MinOrderQuantityUnit';
    enumValues: 'BASE' | 'QUOTE';
  };
  MutationRoot: {
    kind: 'OBJECT';
    name: 'MutationRoot';
    fields: {
      cancelAllOrders: {
        name: 'cancelAllOrders';
        type: { kind: 'SCALAR'; name: 'VenueId'; ofType: null };
      };
      cancelOrder: {
        name: 'cancelOrder';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      cancelOrders: {
        name: 'cancelOrders';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
            };
          };
        };
      };
      createApiKey: {
        name: 'createApiKey';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'ApiKey'; ofType: null };
        };
      };
      createMmAlgo: {
        name: 'createMmAlgo';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      createOrder: {
        name: 'createOrder';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      createOrders: {
        name: 'createOrders';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
            };
          };
        };
      };
      createPovAlgo: {
        name: 'createPovAlgo';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      createSmartOrderRouterAlgo: {
        name: 'createSmartOrderRouterAlgo';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      createSpreadAlgo: {
        name: 'createSpreadAlgo';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      createTelegramApiKey: {
        name: 'createTelegramApiKey';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'ApiKey'; ofType: null };
        };
      };
      createTwapAlgo: {
        name: 'createTwapAlgo';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      previewSmartOrderRouterAlgo: {
        name: 'previewSmartOrderRouterAlgo';
        type: { kind: 'OBJECT'; name: 'AlgoPreview'; ofType: null };
      };
      removeApiKey: {
        name: 'removeApiKey';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
        };
      };
      removeTelegramApiKeys: {
        name: 'removeTelegramApiKeys';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
        };
      };
      sendAlgoControlCommand: {
        name: 'sendAlgoControlCommand';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      setCredentials: {
        name: 'setCredentials';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
        };
      };
      updateMarket: {
        name: 'updateMarket';
        type: { kind: 'OBJECT'; name: 'Market'; ofType: null };
      };
    };
  };
  OmsOrderUpdate: {
    kind: 'OBJECT';
    name: 'OmsOrderUpdate';
    fields: {
      avgFillPrice: {
        name: 'avgFillPrice';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      filledQty: {
        name: 'filledQty';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      state: {
        name: 'state';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'ENUM'; name: 'OrderStateFlags'; ofType: null };
            };
          };
        };
      };
    };
  };
  OptionsMarketSnapshot: {
    kind: 'OBJECT';
    name: 'OptionsMarketSnapshot';
    fields: {
      askIv: {
        name: 'askIv';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      bidIv: {
        name: 'bidIv';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      delta: {
        name: 'delta';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      gamma: {
        name: 'gamma';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      market: {
        name: 'market';
        type: { kind: 'OBJECT'; name: 'Market'; ofType: null };
      };
      marketId: {
        name: 'marketId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
      };
      openInterest: {
        name: 'openInterest';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      rho: {
        name: 'rho';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      theta: {
        name: 'theta';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      undPrice: {
        name: 'undPrice';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      underlying: {
        name: 'underlying';
        type: { kind: 'OBJECT'; name: 'Product'; ofType: null };
      };
      underlyingId: {
        name: 'underlyingId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'ProductId'; ofType: null };
        };
      };
      vega: {
        name: 'vega';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
    };
  };
  Order: {
    kind: 'OBJECT';
    name: 'Order';
    fields: {
      accountId: {
        name: 'accountId';
        type: { kind: 'SCALAR'; name: 'AccountId'; ofType: null };
      };
      dir: {
        name: 'dir';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Dir'; ofType: null };
        };
      };
      id: {
        name: 'id';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      market: {
        name: 'market';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Market'; ofType: null };
        };
      };
      marketId: {
        name: 'marketId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
      };
      orderType: {
        name: 'orderType';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'UNION'; name: 'OrderType'; ofType: null };
        };
      };
      quantity: {
        name: 'quantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      quoteId: {
        name: 'quoteId';
        type: { kind: 'SCALAR'; name: 'Str'; ofType: null };
      };
      source: {
        name: 'source';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'ENUM'; name: 'OrderSource'; ofType: null };
        };
      };
      timeInForce: {
        name: 'timeInForce';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'TimeInForce'; ofType: null };
        };
      };
    };
  };
  OrderId: string;
  OrderLog: {
    kind: 'OBJECT';
    name: 'OrderLog';
    fields: {
      avgFillPrice: {
        name: 'avgFillPrice';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      filledQty: {
        name: 'filledQty';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      order: {
        name: 'order';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Order'; ofType: null };
        };
      };
      orderState: {
        name: 'orderState';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'ENUM'; name: 'OrderStateFlags'; ofType: null };
            };
          };
        };
      };
      rejectReason: {
        name: 'rejectReason';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      timestamp: {
        name: 'timestamp';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
    };
  };
  OrderSource: {
    name: 'OrderSource';
    enumValues:
      | 'ALGO'
      | 'API'
      | 'CLI'
      | 'EXTERNAL'
      | 'GUI'
      | 'OTHER'
      | 'TELEGRAM';
  };
  OrderStateFlags: {
    name: 'OrderStateFlags';
    enumValues:
      | 'ACKED'
      | 'CANCELED'
      | 'CANCELING'
      | 'FILLED'
      | 'OPEN'
      | 'OUT'
      | 'REJECTED'
      | 'STALE';
  };
  OrderType: {
    kind: 'UNION';
    name: 'OrderType';
    fields: {};
    possibleTypes:
      | 'LimitOrderType'
      | 'StopLossLimitOrderType'
      | 'TakeProfitLimitOrderType';
  };
  Orderflow: {
    kind: 'UNION';
    name: 'Orderflow';
    fields: {};
    possibleTypes:
      | 'AberrantFill'
      | 'Ack'
      | 'Cancel'
      | 'CancelAll'
      | 'Fill'
      | 'OmsOrderUpdate'
      | 'Order'
      | 'Out'
      | 'Reject';
  };
  Out: {
    kind: 'OBJECT';
    name: 'Out';
    fields: {
      order: {
        name: 'order';
        type: { kind: 'OBJECT'; name: 'Order'; ofType: null };
      };
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
    };
  };
  PoolMarketKind: {
    kind: 'OBJECT';
    name: 'PoolMarketKind';
    fields: {
      products: {
        name: 'products';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'Product'; ofType: null };
            };
          };
        };
      };
    };
  };
  Position: {
    kind: 'OBJECT';
    name: 'Position';
    fields: {
      account: {
        name: 'account';
        type: { kind: 'OBJECT'; name: 'Account'; ofType: null };
      };
      accountId: {
        name: 'accountId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'AccountId'; ofType: null };
        };
      };
      averagePrice: {
        name: 'averagePrice';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      breakEvenPrice: {
        name: 'breakEvenPrice';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      dir: {
        name: 'dir';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Dir'; ofType: null };
        };
      };
      liquidationPrice: {
        name: 'liquidationPrice';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      market: {
        name: 'market';
        type: { kind: 'OBJECT'; name: 'Market'; ofType: null };
      };
      marketId: {
        name: 'marketId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
      };
      quantity: {
        name: 'quantity';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      tradeDate: {
        name: 'tradeDate';
        type: { kind: 'SCALAR'; name: 'Date'; ofType: null };
      };
      tradeTime: {
        name: 'tradeTime';
        type: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
      };
      venue: {
        name: 'venue';
        type: { kind: 'OBJECT'; name: 'Venue'; ofType: null };
      };
      venueId: {
        name: 'venueId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'VenueId'; ofType: null };
        };
      };
    };
  };
  PovAlgoOrder: {
    kind: 'OBJECT';
    name: 'PovAlgoOrder';
    fields: {
      accountId: {
        name: 'accountId';
        type: { kind: 'SCALAR'; name: 'AccountId'; ofType: null };
      };
      dir: {
        name: 'dir';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Dir'; ofType: null };
        };
      };
      endTime: {
        name: 'endTime';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
      market: {
        name: 'market';
        type: { kind: 'OBJECT'; name: 'Market'; ofType: null };
      };
      marketId: {
        name: 'marketId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
      };
      maxQuantity: {
        name: 'maxQuantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      minOrderQuantity: {
        name: 'minOrderQuantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      name: {
        name: 'name';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      takeThroughFrac: {
        name: 'takeThroughFrac';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      targetVolumeFrac: {
        name: 'targetVolumeFrac';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
    };
  };
  PovAlgoStatus: {
    kind: 'OBJECT';
    name: 'PovAlgoStatus';
    fields: {
      creationTime: {
        name: 'creationTime';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
      fractionComplete: {
        name: 'fractionComplete';
        type: { kind: 'SCALAR'; name: 'Float'; ofType: null };
      };
      marketVolume: {
        name: 'marketVolume';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      order: {
        name: 'order';
        type: { kind: 'OBJECT'; name: 'PovAlgoOrder'; ofType: null };
      };
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      quantityFilled: {
        name: 'quantityFilled';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      realizedVolumeFrac: {
        name: 'realizedVolumeFrac';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      status: {
        name: 'status';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'ENUM'; name: 'AlgoRunningStatus'; ofType: null };
        };
      };
    };
  };
  Product: {
    kind: 'OBJECT';
    name: 'Product';
    fields: {
      expiration: {
        name: 'expiration';
        type: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
      };
      id: {
        name: 'id';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'ProductId'; ofType: null };
        };
      };
      kind: {
        name: 'kind';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      markUsd: {
        name: 'markUsd';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      multiplier: {
        name: 'multiplier';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      name: {
        name: 'name';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      optionType: {
        name: 'optionType';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      strike: {
        name: 'strike';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      underlying: {
        name: 'underlying';
        type: { kind: 'OBJECT'; name: 'Product'; ofType: null };
      };
    };
  };
  ProductId: string;
  QueryRoot: {
    kind: 'OBJECT';
    name: 'QueryRoot';
    fields: {
      accountSummaries: {
        name: 'accountSummaries';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: {
                kind: 'OBJECT';
                name: 'AccountSummaries';
                ofType: null;
              };
            };
          };
        };
      };
      accountSummariesForCpty: {
        name: 'accountSummariesForCpty';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'AccountSummaries'; ofType: null };
        };
      };
      accounts: {
        name: 'accounts';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'Account'; ofType: null };
            };
          };
        };
      };
      algoLog: {
        name: 'algoLog';
        type: { kind: 'OBJECT'; name: 'AlgoLog'; ofType: null };
      };
      algoOrder: {
        name: 'algoOrder';
        type: { kind: 'OBJECT'; name: 'AlgoOrder'; ofType: null };
      };
      algoStatus: {
        name: 'algoStatus';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'AlgoStatus'; ofType: null };
            };
          };
        };
      };
      bookSnapshot: {
        name: 'bookSnapshot';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Book'; ofType: null };
        };
      };
      cmeProductGroupInfos: {
        name: 'cmeProductGroupInfos';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: {
                kind: 'OBJECT';
                name: 'CmeProductGroupInfo';
                ofType: null;
              };
            };
          };
        };
      };
      coinInfo: {
        name: 'coinInfo';
        type: { kind: 'OBJECT'; name: 'CoinInfo'; ofType: null };
      };
      coinInfos: {
        name: 'coinInfos';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'CoinInfo'; ofType: null };
            };
          };
        };
      };
      cptys: {
        name: 'cptys';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'CptyInfo'; ofType: null };
            };
          };
        };
      };
      fills: {
        name: 'fills';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Fills'; ofType: null };
        };
      };
      filterMarkets: {
        name: 'filterMarkets';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'Market'; ofType: null };
            };
          };
        };
      };
      historicalCandles: {
        name: 'historicalCandles';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'CandleV1'; ofType: null };
            };
          };
        };
      };
      listApiKeys: {
        name: 'listApiKeys';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'ApiKey'; ofType: null };
            };
          };
        };
      };
      market: {
        name: 'market';
        type: { kind: 'OBJECT'; name: 'Market'; ofType: null };
      };
      marketSnapshot: {
        name: 'marketSnapshot';
        type: { kind: 'OBJECT'; name: 'MarketSnapshot'; ofType: null };
      };
      markets: {
        name: 'markets';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: { kind: 'OBJECT'; name: 'Market'; ofType: null };
          };
        };
      };
      marketsSnapshots: {
        name: 'marketsSnapshots';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'MarketSnapshot'; ofType: null };
            };
          };
        };
      };
      me: {
        name: 'me';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Me'; ofType: null };
        };
      };
      mmAlgoOrder: {
        name: 'mmAlgoOrder';
        type: { kind: 'OBJECT'; name: 'MMAlgoOrder'; ofType: null };
      };
      mmAlgoStatus: {
        name: 'mmAlgoStatus';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'MMAlgoStatus'; ofType: null };
            };
          };
        };
      };
      openOrders: {
        name: 'openOrders';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'OrderLog'; ofType: null };
            };
          };
        };
      };
      optionsMarketSnapshots: {
        name: 'optionsMarketSnapshots';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: {
                kind: 'OBJECT';
                name: 'OptionsMarketSnapshot';
                ofType: null;
              };
            };
          };
        };
      };
      order: {
        name: 'order';
        type: { kind: 'OBJECT'; name: 'OrderLog'; ofType: null };
      };
      outedOrders: {
        name: 'outedOrders';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'OrderLog'; ofType: null };
            };
          };
        };
      };
      povOrder: {
        name: 'povOrder';
        type: { kind: 'OBJECT'; name: 'PovAlgoOrder'; ofType: null };
      };
      povStatus: {
        name: 'povStatus';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'PovAlgoStatus'; ofType: null };
            };
          };
        };
      };
      product: {
        name: 'product';
        type: { kind: 'OBJECT'; name: 'Product'; ofType: null };
      };
      products: {
        name: 'products';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: { kind: 'OBJECT'; name: 'Product'; ofType: null };
          };
        };
      };
      route: {
        name: 'route';
        type: { kind: 'OBJECT'; name: 'Route'; ofType: null };
      };
      routes: {
        name: 'routes';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'Route'; ofType: null };
            };
          };
        };
      };
      smartOrderRouterOrder: {
        name: 'smartOrderRouterOrder';
        type: { kind: 'OBJECT'; name: 'SmartOrderRouterOrder'; ofType: null };
      };
      smartOrderRouterStatus: {
        name: 'smartOrderRouterStatus';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: {
                kind: 'OBJECT';
                name: 'SmartOrderRouterStatus';
                ofType: null;
              };
            };
          };
        };
      };
      spreadAlgoOrder: {
        name: 'spreadAlgoOrder';
        type: { kind: 'OBJECT'; name: 'MMAlgoOrder'; ofType: null };
      };
      spreadAlgoStatus: {
        name: 'spreadAlgoStatus';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'MMAlgoStatus'; ofType: null };
            };
          };
        };
      };
      tcaBalancePnl: {
        name: 'tcaBalancePnl';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'TcaBalancePnlV1'; ofType: null };
            };
          };
        };
      };
      tcaBalancePnlTimeseries: {
        name: 'tcaBalancePnlTimeseries';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'TcaPnlV1'; ofType: null };
            };
          };
        };
      };
      tcaMarks: {
        name: 'tcaMarks';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'TcaMarksV1'; ofType: null };
            };
          };
        };
      };
      tcaSummary: {
        name: 'tcaSummary';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'TcaSummaryV1'; ofType: null };
            };
          };
        };
      };
      twapOrder: {
        name: 'twapOrder';
        type: { kind: 'OBJECT'; name: 'TwapOrder'; ofType: null };
      };
      twapStatus: {
        name: 'twapStatus';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'TwapStatus'; ofType: null };
            };
          };
        };
      };
      venue: {
        name: 'venue';
        type: { kind: 'OBJECT'; name: 'Venue'; ofType: null };
      };
      venues: {
        name: 'venues';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'Venue'; ofType: null };
            };
          };
        };
      };
      version: {
        name: 'version';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
    };
  };
  Reason: {
    name: 'Reason';
    enumValues:
      | 'ALGO_PAUSED'
      | 'ALGO_STOPPED'
      | 'CANCEL_PENDING'
      | 'MAX_POSITION'
      | 'MIN_POSITION'
      | 'NO_ASK'
      | 'NO_BID'
      | 'NO_REFERENCE_PRICE'
      | 'NO_REFERENCE_SIZE'
      | 'OPEN_ORDER_OUTSIDE_TOLERANCE'
      | 'OPEN_ORDER_WITHIN_TOLERANCE'
      | 'WITHIN_FILL_LOCKOUT'
      | 'WITHIN_ORDER_LOCKOUT'
      | 'WITHIN_REJECT_LOCKOUT';
  };
  ReferencePrice: {
    name: 'ReferencePrice';
    enumValues: 'BID_ASK' | 'HEDGE_MARKET_BID_ASK' | 'MID';
  };
  Reject: {
    kind: 'OBJECT';
    name: 'Reject';
    fields: {
      order: {
        name: 'order';
        type: { kind: 'OBJECT'; name: 'Order'; ofType: null };
      };
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      reason: {
        name: 'reason';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
    };
  };
  RfqResponse: {
    kind: 'OBJECT';
    name: 'RfqResponse';
    fields: {
      buy: {
        name: 'buy';
        type: { kind: 'OBJECT'; name: 'RfqResponseSide'; ofType: null };
      };
      market: {
        name: 'market';
        type: { kind: 'OBJECT'; name: 'Market'; ofType: null };
      };
      marketId: {
        name: 'marketId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
      };
      sell: {
        name: 'sell';
        type: { kind: 'OBJECT'; name: 'RfqResponseSide'; ofType: null };
      };
    };
  };
  RfqResponseSide: {
    kind: 'OBJECT';
    name: 'RfqResponseSide';
    fields: {
      price: {
        name: 'price';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      quantity: {
        name: 'quantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      quoteId: {
        name: 'quoteId';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
    };
  };
  Route: {
    kind: 'OBJECT';
    name: 'Route';
    fields: {
      id: {
        name: 'id';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'RouteId'; ofType: null };
        };
      };
      name: {
        name: 'name';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Str'; ofType: null };
        };
      };
    };
  };
  RouteId: string;
  SmartOrderRouterOrder: {
    kind: 'OBJECT';
    name: 'SmartOrderRouterOrder';
    fields: {
      base: {
        name: 'base';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Product'; ofType: null };
        };
      };
      dir: {
        name: 'dir';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Dir'; ofType: null };
        };
      };
      executionTimeLimitMs: {
        name: 'executionTimeLimitMs';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Int'; ofType: null };
        };
      };
      limitPrice: {
        name: 'limitPrice';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      markets: {
        name: 'markets';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'Market'; ofType: null };
            };
          };
        };
      };
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      parentOrderId: {
        name: 'parentOrderId';
        type: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
      };
      quote: {
        name: 'quote';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Product'; ofType: null };
        };
      };
      targetSize: {
        name: 'targetSize';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
    };
  };
  SmartOrderRouterStatus: {
    kind: 'OBJECT';
    name: 'SmartOrderRouterStatus';
    fields: {
      order: {
        name: 'order';
        type: { kind: 'OBJECT'; name: 'SmartOrderRouterOrder'; ofType: null };
      };
      status: {
        name: 'status';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'AlgoStatus'; ofType: null };
        };
      };
    };
  };
  StopLossLimitOrderType: {
    kind: 'OBJECT';
    name: 'StopLossLimitOrderType';
    fields: {
      limitPrice: {
        name: 'limitPrice';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      triggerPrice: {
        name: 'triggerPrice';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
    };
  };
  Str: string;
  String: string;
  SubscriptionRoot: {
    kind: 'OBJECT';
    name: 'SubscriptionRoot';
    fields: {
      book: {
        name: 'book';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Book'; ofType: null };
        };
      };
      candles: {
        name: 'candles';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'CandleV1'; ofType: null };
        };
      };
      exchangeSpecific: {
        name: 'exchangeSpecific';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: {
                kind: 'OBJECT';
                name: 'ExchangeSpecificUpdate';
                ofType: null;
              };
            };
          };
        };
      };
      fills: {
        name: 'fills';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Fill'; ofType: null };
        };
      };
      orderflow: {
        name: 'orderflow';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'UNION'; name: 'Orderflow'; ofType: null };
        };
      };
      pollAccountSummaries: {
        name: 'pollAccountSummaries';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: {
                kind: 'OBJECT';
                name: 'AccountSummaries';
                ofType: null;
              };
            };
          };
        };
      };
      pollAlgoStatus: {
        name: 'pollAlgoStatus';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'AlgoStatus'; ofType: null };
            };
          };
        };
      };
      pollFills: {
        name: 'pollFills';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'Fills'; ofType: null };
        };
      };
      pollMmAlgoStatus: {
        name: 'pollMmAlgoStatus';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'MMAlgoStatus'; ofType: null };
            };
          };
        };
      };
      pollOpenOrders: {
        name: 'pollOpenOrders';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'OrderLog'; ofType: null };
            };
          };
        };
      };
      pollSorAlgoStatus: {
        name: 'pollSorAlgoStatus';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: {
                kind: 'OBJECT';
                name: 'SmartOrderRouterStatus';
                ofType: null;
              };
            };
          };
        };
      };
      pollSpreadAlgoStatus: {
        name: 'pollSpreadAlgoStatus';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'MMAlgoStatus'; ofType: null };
            };
          };
        };
      };
      pollTwapAlgoStatus: {
        name: 'pollTwapAlgoStatus';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'TwapStatus'; ofType: null };
            };
          };
        };
      };
      rfqs: {
        name: 'rfqs';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'RfqResponse'; ofType: null };
            };
          };
        };
      };
      trades: {
        name: 'trades';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'OBJECT'; name: 'TradeV1'; ofType: null };
        };
      };
    };
  };
  TakeProfitLimitOrderType: {
    kind: 'OBJECT';
    name: 'TakeProfitLimitOrderType';
    fields: {
      limitPrice: {
        name: 'limitPrice';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      triggerPrice: {
        name: 'triggerPrice';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
    };
  };
  TcaBalancePnlV1: {
    kind: 'OBJECT';
    name: 'TcaBalancePnlV1';
    fields: {
      balanceNow: {
        name: 'balanceNow';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      balancePast: {
        name: 'balancePast';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      pnl: {
        name: 'pnl';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      tsNow: {
        name: 'tsNow';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
      tsPast: {
        name: 'tsPast';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
      venue: {
        name: 'venue';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      venueId: {
        name: 'venueId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'VenueId'; ofType: null };
        };
      };
    };
  };
  TcaData: {
    kind: 'OBJECT';
    name: 'TcaData';
    fields: {
      markPrice: {
        name: 'markPrice';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      tcaType: {
        name: 'tcaType';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      tcaValue: {
        name: 'tcaValue';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
    };
  };
  TcaMarksV1: {
    kind: 'OBJECT';
    name: 'TcaMarksV1';
    fields: {
      dir: {
        name: 'dir';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Dir'; ofType: null };
        };
      };
      feeCurrency: {
        name: 'feeCurrency';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      fees: {
        name: 'fees';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      fillId: {
        name: 'fillId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'FillId'; ofType: null };
        };
      };
      market: {
        name: 'market';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      marketId: {
        name: 'marketId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
      };
      multiplier: {
        name: 'multiplier';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      orderId: {
        name: 'orderId';
        type: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
      };
      price: {
        name: 'price';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      quantity: {
        name: 'quantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      source: {
        name: 'source';
        type: { kind: 'SCALAR'; name: 'String'; ofType: null };
      };
      tcaValues: {
        name: 'tcaValues';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: {
            kind: 'LIST';
            name: never;
            ofType: {
              kind: 'NON_NULL';
              name: never;
              ofType: { kind: 'OBJECT'; name: 'TcaData'; ofType: null };
            };
          };
        };
      };
      tradeTime: {
        name: 'tradeTime';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
    };
  };
  TcaPnlV1: {
    kind: 'OBJECT';
    name: 'TcaPnlV1';
    fields: {
      pnl: {
        name: 'pnl';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      ts: {
        name: 'ts';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
    };
  };
  TcaSummaryV1: {
    kind: 'OBJECT';
    name: 'TcaSummaryV1';
    fields: {
      buyNotionalTraded: {
        name: 'buyNotionalTraded';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      fees: {
        name: 'fees';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      label: {
        name: 'label';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      numberOfFills: {
        name: 'numberOfFills';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Int'; ofType: null };
        };
      };
      pnlBps: {
        name: 'pnlBps';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      pnlPriceCurrency: {
        name: 'pnlPriceCurrency';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      sellNotionalTraded: {
        name: 'sellNotionalTraded';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      totalNotionalTraded: {
        name: 'totalNotionalTraded';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
    };
  };
  TimeInForce: {
    kind: 'OBJECT';
    name: 'TimeInForce';
    fields: {
      goodTilDate: {
        name: 'goodTilDate';
        type: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
      };
      instruction: {
        name: 'instruction';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
    };
  };
  TradeV1: {
    kind: 'OBJECT';
    name: 'TradeV1';
    fields: {
      direction: {
        name: 'direction';
        type: { kind: 'SCALAR'; name: 'Dir'; ofType: null };
      };
      price: {
        name: 'price';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      size: {
        name: 'size';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      time: {
        name: 'time';
        type: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
      };
    };
  };
  TwapOrder: {
    kind: 'OBJECT';
    name: 'TwapOrder';
    fields: {
      accountId: {
        name: 'accountId';
        type: { kind: 'SCALAR'; name: 'AccountId'; ofType: null };
      };
      dir: {
        name: 'dir';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Dir'; ofType: null };
        };
      };
      endTime: {
        name: 'endTime';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
      intervalMs: {
        name: 'intervalMs';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Int'; ofType: null };
        };
      };
      market: {
        name: 'market';
        type: { kind: 'OBJECT'; name: 'Market'; ofType: null };
      };
      marketId: {
        name: 'marketId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
      };
      name: {
        name: 'name';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'String'; ofType: null };
        };
      };
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      quantity: {
        name: 'quantity';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      rejectLockoutMs: {
        name: 'rejectLockoutMs';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Int'; ofType: null };
        };
      };
      takeThroughFrac: {
        name: 'takeThroughFrac';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
    };
  };
  TwapStatus: {
    kind: 'OBJECT';
    name: 'TwapStatus';
    fields: {
      creationTime: {
        name: 'creationTime';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'DateTime'; ofType: null };
        };
      };
      fractionComplete: {
        name: 'fractionComplete';
        type: { kind: 'SCALAR'; name: 'Float'; ofType: null };
      };
      order: {
        name: 'order';
        type: { kind: 'OBJECT'; name: 'TwapOrder'; ofType: null };
      };
      orderId: {
        name: 'orderId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'OrderId'; ofType: null };
        };
      };
      quantityFilled: {
        name: 'quantityFilled';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
        };
      };
      realizedTwap: {
        name: 'realizedTwap';
        type: { kind: 'SCALAR'; name: 'Decimal'; ofType: null };
      };
      status: {
        name: 'status';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'ENUM'; name: 'AlgoRunningStatus'; ofType: null };
        };
      };
    };
  };
  UnknownMarketKind: {
    kind: 'OBJECT';
    name: 'UnknownMarketKind';
    fields: {
      unused: {
        name: 'unused';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
        };
      };
    };
  };
  UpdateMarket: {
    kind: 'INPUT_OBJECT';
    name: 'UpdateMarket';
    isOneOf: false;
    inputFields: [
      {
        name: 'isFavorite';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Boolean'; ofType: null };
        };
        defaultValue: null;
      },
      {
        name: 'marketId';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'MarketId'; ofType: null };
        };
        defaultValue: null;
      },
    ];
  };
  UserId: string;
  Venue: {
    kind: 'OBJECT';
    name: 'Venue';
    fields: {
      id: {
        name: 'id';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'VenueId'; ofType: null };
        };
      };
      name: {
        name: 'name';
        type: {
          kind: 'NON_NULL';
          name: never;
          ofType: { kind: 'SCALAR'; name: 'Str'; ofType: null };
        };
      };
    };
  };
  VenueId: string;
};

/** An IntrospectionQuery representation of your schema.
 *
 * @remarks
 * This is an introspection of your schema saved as a file by GraphQLSP.
 * It will automatically be used by `gql.tada` to infer the types of your GraphQL documents.
 * If you need to reuse this data or update your `scalars`, update `tadaOutputLocation` to
 * instead save to a .ts instead of a .d.ts file.
 */
export type introspection = {
  name: never;
  query: 'QueryRoot';
  mutation: 'MutationRoot';
  subscription: 'SubscriptionRoot';
  types: introspection_types;
};

import * as gqlTada from 'gql.tada';

declare module 'gql.tada' {
  interface setupSchema {
    introspection: introspection;
  }
}
