var sjxUpload = {};

sjxUpload.FIELD_FORM_ID = 'sjxUpload_formId';

sjxUpload.getFrameId = function (formId) {
	return 'sjxUpload_iframe_' + formId;
};

sjxUpload.prepareForm = function (formId, callbackName) {
	var frameId = sjxUpload.getFrameId(formId),
		$object = jQuery('#' + formId),
		requestArgs = JSON.stringify([formId]),
		element,
        attrOrProp = (! $object.prop ? 'attr' : 'prop');

	$object.attr('target', frameId);
	$object.attr('method', 'post');
	$object.attr('enctype', 'multipart/form-data');

	if ($object[attrOrProp]('action') === '') {
		//Only change the submit URI if it's not explicitly set to something
		$object[attrOrProp]('action', Sijax.getRequestUri());
	}

	if (! $object[attrOrProp](Sijax.PARAM_REQUEST)) {
		//Initial registration
		var token = document.head.querySelector("[name~=csrf-token][content]").content
		element = document.createElement('input');
		element.setAttribute('type', 'hidden');
		element.setAttribute('name', Sijax.PARAM_CSRF);
		element.setAttribute('value', token);
		$object.append(element);

		element = document.createElement('input');
		element.setAttribute('type', 'hidden');
		element.setAttribute('name', Sijax.PARAM_REQUEST);
		element.setAttribute('value', callbackName);
		$object.append(element);

		element = document.createElement('input');
		element.setAttribute('type', 'hidden');
		element.setAttribute('name', Sijax.PARAM_ARGS);
		element.setAttribute('value', requestArgs);
		$object.append(element);
	} else {
		//The fields are already created, let's just "refresh" their contents
		$object.find('input[name=' + Sijax.PARAM_REQUEST + ']').val(callbackName);
		$object.find('input[name=' + Sijax.PARAM_ARGS + ']').val(requestArgs);
	}
};

sjxUpload.resetForm = function (formId) {
	var $form = jQuery('#' + formId),
		callbackName = $form.find('input[name=' + Sijax.PARAM_REQUEST + ']').val();

	$form[0].reset();

	sjxUpload.prepareForm(formId, callbackName);
};

sjxUpload.registerForm = function (params) {

};

sjxUpload.processResponse = function (formId, commandsArray) {
	Sijax.processCommands(commandsArray);
};
