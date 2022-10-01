CREATE OR REPLACE PROCEDURE ADD_RESERVATION(
	v_total_amount number,
	v_qty_customers number,
	v_reservation_date timestamp,
	v_check_in DATE,
	v_check_out DATE,
	v_department_id NUMBER,
	v_services varchar2,
	v_user_id NUMBER,
	v_salida OUT number
)IS 
BEGIN 
	INSERT INTO reservation(STATUS,TOTAL_AMOUNT,RESERVATION_AMOUNT,DIFFERENCE_AMOUNT,QTY_CUSTOMERS,RESERVATION_DATE,CHECK_IN,CHECK_OUT,DEPARTMENT_ID,SERVICES,USER_ID)
	values(v_total_amount, v_qty_customers, v_reservation_date, v_check_in, v_check_out, v_department_id, v_services, v_user_id, v_salida )

	v_salida:=1;

	exception

	when others then
		v_salida:=0;
END;

INSERT INTO reservation(
ID,
STATUS,
TOTAL_AMOUNT,
RESERVATION_AMOUNT,
DIFFERENCE_AMOUNT,
QTY_CUSTOMERS,
RESERVATION_DATE,
CHECK_IN,
CHECK_OUT,
DEPARTMENT_ID,
SERVICES,
USER_ID)
values(
ISEQ$$_77445.nextval,
'reservado',
100000,
10000,
90000,
2,
'2022-09-28 12:42:23.701 +0000', 
'28-09-22', 
'28-09-22', 
21, 
'[transporte, jugo]',
21
);
--------
CREATE OR REPLACE PROCEDURE ADD_RESERVATION(
 V_RESERVATION_DATE TIMESTAMP,
 V_CHECK_IN DATE,
 V_CHECK_OUT DATE,
 V_DEPARTMENT_ID NUMBER,
 V_DIFFERENCE_AMOUNT NUMBER,
 V_QTY_CUSTOMERS NUMBER,
 V_RESERVATION_AMOUNT NUMBER,
 V_SERVICES NUMBER,
 V_STATUS varchar2,
 V_TOTAL_AMOUNT NUMBER,
 V_USER_ID NUMBER
 v_salida number
)IS 
BEGIN 
	INSERT INTO reservation(RESERVATION_DATE
		CHECK_IN,
		CHECK_OUT,
		DEPARTMENT_ID,
		DIFFERENCE_AMOUNT,
		QTY_CUSTOMERS,
		RESERVATION_AMOUNT,
		SERVICES,
		STATUS,
		TOTAL_AMOUNT,
		USER_ID	)
	values(
		V_RESERVATION_DATE,
		V_CHECK_IN,
		V_CHECK_OUT,
		V_DEPARTMENT_ID,
		V_DIFFERENCE_AMOUNT,
		V_QTY_CUSTOMERS,
		V_RESERVATION_AMOUNT,
		V_SERVICES,
		V_STATUS,
		V_TOTAL_AMOUNT,
		V_USER_ID)
	v_salida:=1;

	exception

	when others then
		v_salida:=0;
END;

COMMIT;

-- para conocer nombres de las seq id creadas auto x django
select sequence_name from user_sequences;
select sequence_name from TURISMO_REAL_DEV;



INSERT INTO reservation(
V_RESERVATION_DATE,
V_CHECK_IN,
V_CHECK_OUT,
V_DEPARTMENT_ID,
V_DIFFERENCE_AMOUNT,
V_QTY_CUSTOMERS,
V_RESERVATION_AMOUNT,
V_SERVICES,
V_STATUS,
V_TOTAL_AMOUNT,
V_USER_ID)
values(
'28-09-22', 
'01-10-22', 
'05-10-22', 
21, 
90000,
2,
10000,
8,
'reservado',
100000,
1
);

------
---------------------
-- AÑADIR RESERVA
----------------------
CREATE OR REPLACE PROCEDURE ADD_RESERVATION(
	v_check_in DATE,
	v_check_out DATE,
	v_qty_customers number,
	v_reservation_amount number,
	v_total_amount number,
	v_user_id NUMBER,
	v_department__disponibility_id NUMBER,
	v_salida OUT number
)IS 
BEGIN 
	INSERT INTO reservation(check_in,check_out,qty_customers,reservation_amount,total_amount,user_id,department__disponibility_id)
	values(v_check_in,v_check_out,v_qty_customers,v_reservation_amount,v_total_amount,v_user_id,v_department__disponibility_id)

	v_salida:=1;
	
	UPDATE DEPARTMENT_DISPONIBILITY 
	SET 
		STATUS = 'reservado',
		START_RESERVATION = v_check_in,
		FINISH_RESERVATION = v_check_out
	WHERE DEPARTMENT_ID  = v_department_id
	exception

	INSERT INTO RESERVATION_DETAILS(EXTRA_SERVICE_ID, RESERVATION_ID)
	VALUES()

	when others then
		v_salida:=0;
END;