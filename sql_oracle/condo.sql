create table condo (
   condo_base_bbl       varchar2(10)
  ,condo_billing_bbl    varchar2(10)
  ,primary key (condo_base_bbl, condo_billing_bbl)
);