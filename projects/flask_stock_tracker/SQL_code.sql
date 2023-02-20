CREATE TABLE masy3540_co_stock (
    DT          VARCHAR2(50 BYTE) NOT NULL,
    OPEN        NUMBER,
    HIGH        NUMBER,
    LOW         NUMBER,
    CLOSE       NUMBER,
    VOLUME      NUMBER,
    DIVIDENDS   NUMBER,
    STOCK_SPLIT NUMBER
);

DROP TABLE masy3540_co_stock

SELECT * FROM masy3540_co_stock

TRUNCATE TABLE masy3540_co_stock
